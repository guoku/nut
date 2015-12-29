require([
        'libs/polyfills',
        'jquery',
        'subapp/yearseller/header',
        'subapp/yearseller/linkscroll',
        'subapp/yearseller/share'
    ],
    function(polyfill,
             $,
             YearSellerHeader,
             AnchorScroller,
             ShareHanlder

    ){

        var sellerHeader = new YearSellerHeader();
        var anchorScroller = new AnchorScroller('.sections-titles-wrapper li a');
        var shareHandler = new ShareHanlder();
        console.log('in year seller app');

    });
