const app = Vue.createApp({
    data() {
        return {
            word: '',
            title: 'Poltwittex',
            showParties: false,
            showPoliticsFromParty: false,
            showPoliticsFromSejm: false,
            showPoliticsWords: false,
            showPartyWords: false,
            showSejmWords: true,
            timeline: 1,
            party: '',
            tweets: [
            ],
            politics: [],
            parties: []
        }
    },
    methods: {
        sumitSearch(word) {
            this.tweets = this.tweets.filter(tweet => tweet.word.includes(word))
        },
        async getSejm() {
            this.showPartyWords = false;
            this.showPoliticsWords = false;
            this.showSejmWords = true;
            resetState(this);
            this.tweets = []
            const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/words/sejm', { params: { limit: 200 } })
            for (const data of response.data) {
                for (const politician of politiciansResponse.data) {
                    if (data.politician_id === politician.twitter_id) {
                        this.tweets.push({ name: politician.name, word: data.word, count: data.count });
                    }
                }
            }

        },
        async getParty() {
            this.showPartyWords = true;
            this.showPoliticsWords = false;
            this.showSejmWords = false;
            const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/parties')
            this.parties = response.data
            this.showPoliticsFromSejm = false;
            this.showParties = !this.showParties;
        },
        async getPoselsFromParty(party) {
            this.showPartyWords = false;
            this.showPoliticsWords = true;
            this.showSejmWords = false;
            const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/politicians', { params: { 'party': party.id } })
            this.politics = response.data
            this.showPoliticsFromSejm = false;
            this.party = party
            this.showPoliticsFromParty = true;
        },
        async getPoselsFromSejm() {
            this.showPartyWords = false;
            this.showPoliticsWords = true;
            this.showSejmWords = false;
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
        },
        changeTimeline(time) {
            console.log(time);
            this.timeline = time;
        }
    },
    async created() {
        const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/words', { params: { limit: 200 } })
        const politiciansResponse = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/politicians')
        for (const data of response.data) {
            for (const politician of politiciansResponse.data) {
                if (data.politician_id === politician.twitter_id) {
                    this.tweets.push({ name: politician.name, word: data.word, count: data.count });
                }
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

