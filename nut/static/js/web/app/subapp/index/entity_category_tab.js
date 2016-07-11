
define(['jquery', 'subapp/index/selection_entity_slick'], function(
    $,SelectionEntitySlick
){
    var EntityCategoryTab= SelectionEntitySlick.extend({
        init: function () {
            this.$entity_container = $('.latest-entity-wrapper');
            this.init_slick();
            this.initHoverCategory();
            console.log('selection entity tab view begin');
        },
        initHoverCategory:function(){
            $('#entity_category_container .category-list-item').mouseenter(this.handleHoverCategory.bind(this));

        },
        handleHoverCategory:function(event){
            var that = this;
            var dataValue = $(event.target).attr('data-value');
            that.postAjaxRequest(dataValue);
        },
        postAjaxRequest:function(dataValue){
             var data = {
                    'dataValue': dataValue
            };
            $.when(
                $.ajax({
                    cache:true,
                    type:"get",
                    url: '/index_selection_entity_tag/',
                    data: data,
                    dataType:"json"
                })
            ).then(
                this.postSuccess.bind(this),
                this.postFail.bind(this)
            );
        },
        postSuccess:function(result){
            console.log('post request success.');
            var status = parseInt(result.status);
            if(status == 1){
                 this.showContent($(result.data));
            }else{
                this.showFail(result);
            }
        },
        postFail:function(result){
            console.log('post fail');
        },
        showFail:function(result){
            console.log('ajax data failed');
        },
        showContent: function(elemList){
            console.log('ajax data success');
            this.$entity_container.empty();
            this.$entity_container.append(elemList);
            this.init_slick();
        }
    });
    return EntityCategoryTab;
});



