define(['libs/Class', 'jquery', 'underscore'], function(Class,$,_){

    //http://open.weibo.com/blog/%E5%88%86%E4%BA%AB%E6%8C%89%E9%92%AE%E7%9A%84%E5%89%8D%E4%B8%96%E4%BB%8A%E7%94%9F-%E2%80%93-%E7%8E%A9%E8%BD%AC%E6%96%B0%E6%B5%AA%E5%BE%AE%E5%8D%9A%E5%88%86%E4%BA%AB%E6%8C%89%E9%92%AE

    var ShareHanlder = Class.extend({
        init: function(){

            this.share_service_url = 'http://service.weibo.com/share/share.php';

            this.shareOptions = {
                share_url : location.href,
                type:'6',
                count:'0',
                appkey:'1459383851',
                ralateUid:'2179686555',
                language:'zh_cn',
                rnd : new Date().valueOf(),
            };



            this.setupShareTrigger();

        },

        setupShareTrigger: function(){
            this.setUpSharePage();

            $('.seller-cross-screen .share-btn')
                .each(this.setupSharePageBtn.bind(this));

            $('.sellers-share .share-btn')
                .each(this.setupShareSellerBtn.bind(this));

        },

        setupSharePageBtn: function(ele){
            console.log(ele);
            var options = _.clone(this.shareOptions);
                options.title = 'this is page sharing title';
                options.pic = 'http://static.guoku.com/static/v4/6f848cd0324e89b80d3c2c776a9d29c5ebee4005/images/gklogo2015.png';

            var pList   = [];

            for (var key in options){
                pList.push(key+'='+encodeURIComponent(options[key]));
            }
            ele.href = this.share_service_url + '?' + pList.join('&');
            return;

        },
        setupShareSellerBtn: function(ele){
            console.log(ele);
            var options = _.clone(this.shareOptions);
                options.title = this.getSellerShareTitle(ele);
                options.pic = this.getShellerSharePic(ele);

        },

        getSellerShareTitle: function(ele){
            return 'test title';
        },
        getSellerSharePic: function(ele){
            return 'test pic';
        }

    });
    return ShareHanlder
});
