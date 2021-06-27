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
            timeline: 30,
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
            this.tweets = [];
            console.log(this.timeline)
            const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/words/sejm', { params: { minusDays: this.timeline, limit: 1000 } })
            for (const data of response.data) {
                this.tweets.push({ word: data.word, count: data.count });
            }

        },
        async getParty() {
            this.showPartyWords = true;
            this.showPoliticsWords = false;
            this.showSejmWords = false;
            this.showPoliticsFromSejm = false;
            this.showParties = !this.showParties;

            this.tweets = []
            const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/parties')
            this.parties = response.data
            for (const party of this.parties) {
                const partyWords = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/words/party', { params: { party: party.id, limit: 1000, minusDays: this.timeline } })
                for (const data of partyWords.data) {
                    this.tweets.push({ name: party.name, word: data.word, count: data.count });
                }
            }
            // this.tweets.sort((a,b)=> (a.count>b.count)?1:-1)

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
            const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/words', { params: { 'politic': politic.twitter_id, minusDays: this.timeline } })
            for (const data of response.data) {
                this.tweets.push({ name: politic.name, word: data.word, count: data.count });
            }
        },
        changeTimeline(time) {
            this.timeline = time;
        }
    },
    async created() {
        console.log(this);
        this.showPartyWords = false;
        this.showPoliticsWords = false;
        this.showSejmWords = true;
        resetState(this);
        this.tweets = [];
        const response = await axios.get('https://poltweetex.northeurope.cloudapp.azure.com/words/sejm', { params: { limit: 1000, minusDays: this.timeline } })
        for (const data of response.data) {
            this.tweets.push({ word: data.word, count: data.count });
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

