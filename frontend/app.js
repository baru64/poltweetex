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
                { name: 'Filip', surname: 'Piwowarczyk', party: 'Husaria', word: 'Kurde', lastTT: '20:10 2021.03.04', count: 3 },
                { name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'SIemanko', lastTT: '20:10 2021.03.04', count: 5 },
                { name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'Elo', lastTT: '20:10 2021.03.04', count: 999 },
                { name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'Yo', lastTT: '20:10 2021.03.04', count: 123 },
                { name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'Mordo', lastTT: '20:10 2021.03.04', count: -12 },
                { name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'Co', lastTT: '20:10 2021.03.04', count: 0 },
                { name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'Tu', lastTT: '20:10 2021.03.04', count: -123 },
                { name: 'Filip', surname: 'Piwowarczyk', party: 'PO', word: 'Robisz', lastTT: '20:10 2021.03.04', count: 1.5 },
            ],
            politics: [
                { name: 'Jan', surname: 'Brzechwa', id: 12343321 },
                { name: 'Karol', surname: 'Krawczyk', id: 12343321 },
                { name: 'Twoja', surname: 'Mama', id: 12343321 },
            ],
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
        getPoselsFromParty(party) {
            console.log("Get Posels in Party from DB");
            this.showPoliticsFromSejm = false;
            this.party = party
            console.log(party.id)
            this.showPoliticsFromParty = true;
        },
        async getPoselsFromSejm() {
            const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/politicians')
            console.log(response);
            this.politics = response.data
            this.party = 'Sejmu';
            this.showParties = false;
            this.showPoliticsFromParty = false;
            this.showPoliticsFromSejm = true;

        },
        getPoliticainWords() {
            fetch("http://127.0.0.1:8000/rndtweets")
                .then(response => response.json)
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

