require(['jquery',
          'subapp/topmenu',
          'subapp/gotop',
          'subapp/event/event_entity_loader',
          'bootstrap',
          'subapp/tracker',
          'snowFall'

    ],
    function($,Menu,GoTop,EventEntityLoader,Tracker,snowFall){

        var menu = new Menu();
        var gotop = new GoTop();
        var eventEntityLoader = new EventEntityLoader();
        var tracker_list = [
            {
                selector: '.event-link',
                trigger: 'click',
                category: 'event',
                action: 'event_detail',
                label: 'data-event-title',
                value: 'data-event-id',
                wrapper: '#event_list_page'
            }
        ];

        var tracker = new Tracker(tracker_list);

        //snow();
        function snow(){
            if (/20151225/.test(location.pathname)){
                 $(document).snowfall('clear');
                 $(document).snowfall({shadow : false, round : true,  minSize: 5, maxSize:8,flakeCount : 120});
                 window.setTimeout(snow, 10000);
            }
        }

        snow();

    });