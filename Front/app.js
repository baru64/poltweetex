const app = Vue.createApp({
    data(){
        return{
            word: '',
            title: 'Title',
            sejm: 'Sejm',
            polityk: 'Polityk',
            posel: 'Poseł',
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

const app2 = Vue.createApp({
    data (){
        return {
            tweets: [
                {nr: 1, name: 'Filip', surname: 'Piwowarczyk', party: 'Husaria', word: 'Kurde', lastTT:'20:10 2021.03.04', count: 3},
                {nr: 2, name: 'Filip', surname: 'Piwowarczyk', party: 'Husaria', word: 'Kurde', lastTT:'20:10 2021.03.04', count: 5}
            ]
        }
    },
    methods: {
        reverseMessage() {
            this.message2 = this.message2.split('').reverse().join('');
        }
    }

})
app.mount("#Search")
app2.mount('#Table')

