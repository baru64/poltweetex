

const app = Vue.createApp({
    data (){
        return {
            message: 'Message Injection',
            message2: 'Message in other div'
        }
    }
    

})

const app2 = Vue.createApp({
    data (){
        return {
            message2: 'Message in other div'
        }
    },
    methods: {
        reverseMessage() {
            this.message2 = this.message2.split('').reverse().join('');
        }
    }

})

app.mount('#Message')
app2.mount('#Reverse')
// app1.mount('#Reverse')
// app2.mount('#Request')



