define(['libs/Class'], function (Class) {
    var Tracker = Class.extend({
        init: function (tracker_list) {
            tracker_list.map(function(ele){
                  var selector = ele.selector;
                  var trigger = ele.trigger;
                  $('.'+ selector).on(trigger, function(){
                      return trackerItem(ele);
                     //console.log('event');
                      //var target = event.currentTarget;
                      //var category = $(target).attr(ele.category);
                      //var action = $(target).attr(ele.action);
                      //var opt_label = $(target).attr(ele.label);
                      //var opt_value = $(target).attr(ele.value);
                      // 闭包
                     //_hmt.push('_trackEvent', category, action, opt_label, opt_value);
                  });
                  function trackerItem(ele) {
                      console.log('ele', ele);
                      var target = event.currentTarget;
                      var category = $(target).attr(ele.category);
                      var action = $(target).attr(ele.action);
                      var opt_label = $(target).attr(ele.label);
                      var opt_value = $(target).attr(ele.value);
                       //闭包
                     _hmt.push('_trackEvent', category, action, opt_label, opt_value);
                  }
            });
        }
    });
    return Tracker;
});