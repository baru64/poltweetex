console.log("Vue")

var app = new Vue({
    el: '#Message',
    data :{
        message:'Hello Vue!'
    }
})

var app = new Vue({
    el:`#Reverse`,
    data: {
        message: 'Hello Vue.js!'
    },
    methods: {
        reverseMessage: function(){
            this.message = this.message.split('').reverse().join('');
        }
    }
})

var app = new Vue({
    el: '#Request',
    data:{
        message:'Get google.com'
    },
    methods:{
        getRequest: function(){
            this.message = this.$http.get('google.com');
        }
    }
})