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
        async getSejm() {
            resetState(this);
            this.tweets = []
            const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/words')
            const politiciansResponse = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/politicians')
            for (const data of response.data) {
                for (const politician of politiciansResponse.data) {
                    if (data.politician_id === politician.twitter_id) {
                        this.tweets.push({ name: politician.name, word: data.word, count: data.count });
                    }
                }
            }

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
            this.tweets = []
            const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/words', { params: { 'politic': politic.twitter_id } })
            for (const data of response.data) {
                this.tweets.push({ name: politic.name, word: data.word, count: data.count });
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

