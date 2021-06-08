import * as pulumi from "@pulumi/pulumi";
import * as resources from "@pulumi/azure-native/resources";
import * as storage from "@pulumi/azure-native/storage";
import * as web from "@pulumi/azure-native/web";
import * as sql from "@pulumi/azure-native/sql"

// Create an Azure Resource Group
const resourceGroup = new resources.ResourceGroup("resourceGroup");

// Create an Azure resource (Storage Account)
const storageAccount = new storage.StorageAccount("sa", {
    resourceGroupName: resourceGroup.name,
    kind: storage.Kind.StorageV2,
    sku: {
        name: storage.SkuName.Standard_LRS,
    },
});

// Export the primary key of the Storage Account
const storageAccountKeys = pulumi.all([resourceGroup.name, storageAccount.name]).apply(([resourceGroupName, accountName]) =>
    storage.listStorageAccountKeys({ resourceGroupName, accountName }));
export const primaryStorageKey = storageAccountKeys.keys[0].value;

const dblogin = "dummylogin";
const dbpwd = "asdfnewr134ss3!@11f4265sassdfcxvzew4sf-23"

// Create database server and database
const dbserver = new sql.Server("dbserver2", {
    administratorLogin: dblogin,
    administratorLoginPassword: dbpwd,
    resourceGroupName: resourceGroup.name,
    serverName: "twitterdbserver2",
});


const database = new sql.Database("tweetdb", {
    databaseName: "tweetdb",
    resourceGroupName: resourceGroup.name,
    serverName: dbserver.name,
    sku: {
        name: "S0",
    },
});

const linuxPlan = new web.AppServicePlan("linux-asp", {
    resourceGroupName: resourceGroup.name,
    kind: "Linux",
    sku: {
        name: "Y1",
        tier: "Dynamic",
    },
    reserved: true,
});

const container = new storage.BlobContainer("container", {
    accountName: storageAccount.name,
    resourceGroupName: resourceGroup.name,
    publicAccess: storage.PublicAccess.None,
});

const pythonBlob = new storage.Blob("pythonBlob", {
    resourceGroupName: resourceGroup.name,
    accountName: storageAccount.name,
    containerName: container.name,
    source: new pulumi.asset.FileArchive("./python"),
});

const pythonBlobSignedURL = signedBlobReadUrl(pythonBlob, container, storageAccount, resourceGroup);

const pythonApp = new web.WebApp("httppython", {
    resourceGroupName: resourceGroup.name,
    serverFarmId: linuxPlan.id,
    kind: "FunctionApp",
    siteConfig: {
        appSettings: [
            { name: "runtime", value: "python" },
            { name: "FUNCTIONS_WORKER_RUNTIME", value: "python" },
            { name: "WEBSITE_RUN_FROM_PACKAGE", value: pythonBlobSignedURL },
            { name: "FUNCTIONS_EXTENSION_VERSION", value: "~3" },
            { name: "DATABASE_CONNECTION",
              value: pulumi.all([dbserver.name, database.name]).apply(([server, db]) =>                   
                `Server=tcp:${server}.database.windows.net;initial catalog=${db};user ID=${dblogin};password=${dbpwd};Min Pool Size=0;Max Pool Size=30;Persist Security Info=true;`) }
        ]
    },
});

function signedBlobReadUrl(
    blob: storage.Blob,
    container: storage.BlobContainer,
    account: storage.StorageAccount,
    resourceGroup: resources.ResourceGroup
): pulumi.Output<string> {
    const blobSAS = pulumi.all<string>([blob.name, container.name, account.name, resourceGroup.name]).apply(args =>
        storage.listStorageAccountServiceSAS({
            accountName: args[2],
            protocols: storage.HttpProtocol.Https,
            sharedAccessExpiryTime: "2030-01-01",
            sharedAccessStartTime: "2021-01-01",
            resourceGroupName: args[3],
            resource: storage.SignedResource.C,
            permissions: storage.Permissions.R,
            canonicalizedResource: "/blob/" + args[2] + "/" + args[1],
            contentType: "application/json",
            cacheControl: "max-age=5",
            contentDisposition: "inline",
            contentEncoding: "deflate",
        }));

    return pulumi.interpolate`https://${account.name}.blob.core.windows.net/${container.name}/${blob.name}?${blobSAS.serviceSasToken}`;
}

export const pythonEndpoint = pythonApp.defaultHostName.apply(ep => `https://${ep}/api/apifunction?name=Pulumi`);
