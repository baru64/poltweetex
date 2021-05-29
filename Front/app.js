const app = Vue.createApp({
    data(){
        return {
            word: '',
            title: 'Twitter Of Politics',
            showParties: false,
            showPoliticsFromParty: false,
            showPoliticsFromSejm: false,
            party: '',
            tweets: [
                {name: 'Filip', surname: 'Piwowarczyk', party: 'Husaria', word: 'Kurde', lastTT:'20:10 2021.03.04', count: 3},
                {name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'SIemanko', lastTT:'20:10 2021.03.04', count: 5},
                {name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'Elo', lastTT:'20:10 2021.03.04', count: 999},
                {name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'Yo', lastTT:'20:10 2021.03.04', count: 123},
                {name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'Mordo', lastTT:'20:10 2021.03.04', count:-12},
                {name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'Co', lastTT:'20:10 2021.03.04', count: 0},
                {name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'Tu', lastTT:'20:10 2021.03.04', count: -123},
                {name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'Robisz', lastTT:'20:10 2021.03.04', count: 1.5},
            ],
            politics: [
                {name: 'Jan', surname: 'Brzechwa', id:12343321},
                {name: 'Karol', surname: 'Krawczyk', id:12343321},
                {name: 'Twoja', surname: 'Mama', id:12343321},
            ],
            parties: [
                {name: 'PO'},
                {name: 'PSL'},
                {name: 'LEWICA'},
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

        },
        getSejm(){
            console.log("Get All words in Sejm");
            resetState(this);
        },
        getParty(){
            console.log("Get Words in Party and show Politics of Party");
            this.showParties = !this.showParties;
            this.showPoliticsFromSejm = false;
        },
        getPoselsFromParty(party){
            console.log("Get Posels From");
            this.showPoliticsFromSejm = false;
            this.showPoliticsFromParty = true;
            this.party = party
        },
        getPoselsFromSejm(){
            console.log("Get Posels From Sejm");
            this.party = 'Sejm';
            this.showParties = false;
            this.showPoliticsFromParty = false;
            this.showPoliticsFromSejm = true;
        },
        getPoliticainWords(){
            console.log("Output Politican Words");
        }
    }
});


function resetState(ctx){
    ctx.word = '';
    ctx.party = '';
    ctx.showParties = false;
    ctx.showPoliticsFromParty = false;
    ctx.showPoliticsFromSejm = false;
}
app.mount("#app")

