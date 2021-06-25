const app = Vue.createApp({
    data() {
        return {
            word: '',
            title: 'Twitter Of Politics',
            showParties: false,
            showPoliticsFromParty: false,
            showPoliticsFromSejm: false,
            party: '',
            tweets: [
            ],
            politics: [],
            parties: []
        }
    },
    methods: {
        sumitSearch(word) {
            console.log(word);
            this.word = '';
        },
        getSejm() {
            console.log("Get All words from DB");
            resetState(this);
        },
        async getParty() {
            const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/parties')
            this.parties = response.data
            this.showPoliticsFromSejm = false;
            this.showParties = !this.showParties;
        },
        async getPoselsFromParty(party) {
            const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/politicians', { params: { 'party': party.id } })
            this.politics = response.data
            this.showPoliticsFromSejm = false;
            this.party = party
            this.showPoliticsFromParty = true;
        },
        async getPoselsFromSejm() {
            const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/politicians', { params: { 'party': 0 } })
            this.politics = response.data
            this.party = 'Sejmu';
            this.showParties = false;
            this.showPoliticsFromParty = false;
            this.showPoliticsFromSejm = true;

        },
        async getPoliticainWords(politic) {
            console.log(politic)
            const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/words', { params: { 'politician': politic.twitter_id } })
            for(const data of response.data){
                console.log(data);
                this.tweets.push({name:politic.name,word:data.word,count:data.count});
            }
        }
    }
});


function resetState(ctx) {
    ctx.word = '';
    ctx.party = '';
    ctx.showParties = false;
    ctx.showPoliticsFromParty = false;
    ctx.showPoliticsFromSejm = false;
}
app.mount("#app")

