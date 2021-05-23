const app = Vue.createApp({
    data(){
        return{
            word: '',
            title: 'Title',
            sejm: 'Sejm',
            polityk: 'Polityk',
            posel: 'Poseł',
            tweets: [
                {nr: 1, name: 'Filip', surname: 'Piwowarczyk', party: 'Husaria', word: 'Kurde', lastTT:'20:10 2021.03.04', count: 3},
                {nr: 2, name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'SIemanko', lastTT:'20:10 2021.03.04', count: 5},
                {nr: 3, name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'SIemanko', lastTT:'20:10 2021.03.04', count: 5},
                {nr: 4, name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'SIemanko', lastTT:'20:10 2021.03.04', count: 5},
                {nr: 5, name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'SIemanko', lastTT:'20:10 2021.03.04', count: 5},
                {nr: 6, name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'SIemanko', lastTT:'20:10 2021.03.04', count: 5},
                {nr: 2, name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'SIemanko', lastTT:'20:10 2021.03.04', count: 5},
            ]
        }
        
    },
    methods: {
        sumitSearch(word){
            console.log(word);
            this.word = '';
        },
        changeTitle(buttonName){
            this.title = buttonName;
        }
    }
    

})

app.mount("#app")

