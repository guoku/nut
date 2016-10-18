var BaiduMapManager = Class.extend({
    init: function(){
        console.log('baidu map config');
        this.initBaiduMap();
    },
    initBaiduMap:function(){
          // 百度地图API功能
        var map = new BMap.Map("allmap");
        map.enableScrollWheelZoom();   //启用滚轮放大缩小，默认禁用
        map.enableContinuousZoom();    //启用地图惯性拖拽，默认禁用

        var getInputLng = $('#id_address_lng').val();
        var getInputLat =  $('#id_address_lat').val();
        if(getInputLng && getInputLat){
            var point = new BMap.Point(getInputLng,getInputLat);
            var marker = new BMap.Marker(new BMap.Point(getInputLng,getInputLat));
            map.addOverlay(marker);
            map.centerAndZoom(point,12);
        }else{
            map.centerAndZoom("北京",12);
        }

        //单击添加Marker,并获取和设置经纬度至Form
        map.addEventListener("click",function(e){
            map.clearOverlays(); //清除地图上所有覆盖物
            var marker = new BMap.Marker(new BMap.Point(e.point.lng, e.point.lat)); //创建marker点
            map.addOverlay(marker);    //增加点
            attribute();

            function attribute(){
                var p = marker.getPosition();  //获取marker的位置
                $('#id_address_lng').val(p.lng);
                $('#id_address_lat').val(p.lat);
            }
        });
    }
});


(function($, window, document){
    $(function(){
         var baidu_map_manager = new BaiduMapManager();
    });
})(jQuery, window, document);