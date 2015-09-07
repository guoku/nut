define(function(require){
    "use strict";
    var Writers = require('models/writers');

    function getCreatorSelectOptions(callback){
            var writerList = new Writers();
                writerList.on('reset', function(){
                    var resultList = [];
                    writerList.each(function(writer){
                        resultList.push({val: writer.get('id'), label: writer.get('profile').nickname});
                    });
                    callback(resultList)
                });
                writerList.fetch({reset: true});
        }

    var ArticleDetailFormView = Backbone.Form.extend({

        initialize: function(options){
            Backbone.Form.prototype.initialize.call(this, options);
        },
        saveArticle:function(){
            this.commit();
            this.model.save();
            this.remove();
        },
        cancelEdit:function(){
            console.log('cancel is clicked , captured by form view');
            this.remove();
        },
        tagName: 'form',
        template : _.template($('#id_article_detail_form_template').html()),
        schema: {
            title: {type:'Text', validators:['required']},
            cover: {type:'Imgpicker', validators:['required']},
            creator_id: {type:'Select',options:getCreatorSelectOptions},
            publish: {type:'Select', options:{0: '移除', 1:'草稿' , 2:'发布'}},
            read_count: {type: 'Number', validators:['required']},
            tags:'Text'
        },

    });

    var ArticleListItemView = Backbone.View.extend({
        initialize: function(){
            Backbone.View.prototype.initialize.apply(this,[].slice.call(arguments));
            this.listenTo(this.model, 'sync', this.render);
        },
        tagName: 'tr',
        template : _.template($('#id_article_list_item_template').html()),
        events : {
            'click .edit-content': 'editContent',
            'click .edit-status': 'editAttribute'
        },

        getDetailFormContainer: function(){
             var that = this ;
             bootbox.hideAll();
             bootbox.setDefaults({
                className: 'batch-selection-modal',
                closeButton: false,
                locale:'zh_CN'
            });
            bootbox.dialog({
                title: '文章属性编辑',
                    message:'<div id="article_form_wrapper"></div>',
                    buttons:{
                        success:{
                            label:"保存文章",
                            className: 'btn-success save-article',
                            callback: function(){ that.trigger('modalOK');}
                        },
                        fail:{
                            label:"放弃操作",
                            className:'btn-danger quit-edit',
                            callback: function(){that.trigger('modalCancel');}
                        }
                    }

            });
            return $('#article_form_wrapper');
        },

        editAttribute: function(){
            var articleEditView = new ArticleDetailFormView({
               model: this.model,
            });
            var detailFormContainer = this.getDetailFormContainer();
                detailFormContainer.append(articleEditView.render().$el);

            articleEditView.listenToOnce(this, 'modalOK', articleEditView.saveArticle);
            articleEditView.listenToOnce(this, 'modalCancel', articleEditView.cancelEdit);
        },
        editContent: function(){
            alert('attribute' + this.model.get('id'));
        },
        render: function(){
            this.$el.html(this.template(this.model.toJSON()));
            return this ;
        }

    });

    var ArticleListView = Backbone.View.extend({
        initialize: function(){
            this.listenTo(this.collection, 'reset', this.render);
            this.listenTo(this.collection, 'sync', this.sync);
            this.listContainer = this.$('.list-container');
            this.clearEle(this.listContainer.get());

            this.$page_info = this.$('.page-info');
            this.$total_page = this.$('.total-page-info');
            this.$input_pagenum = this.$('#to_page_num');

            this.collection.fetch({reset:true});
        },
        events:{
            'click .page-action.first': 'goFirstPage',
            'click .page-action.prev':'goPrevPage',
            'click .page-action.next':'goNextPage',
            'change .to_page_num': 'pageNumberChanged'
        },
        pageNumberChanged: function(event){
           var pageNum =  parseInt($(event.target).val());
               if (_.isNumber(pageNum)){
                   this.collection.getPage(pageNum, {reset:true});
               }
        },

        goFirstPage: function(){
            this.collection.getFirstPage({reset: true});
        },

        goPrevPage: function(){
            this.collection.getPreviousPage({reset:true});
        },
        goNextPage:function(){
            this.collection.getNextPage({reset:true});
        },

        render: function(){
            this.clearEle(this.listContainer.get());
            var container = this.listContainer;
            var totalPageNumber = this.collection.state.totalPages;
            this.$page_info.html("第"+this.collection.state.currentPage + "页");
            this.$total_page.html("/共"+(totalPageNumber)+ "页");

            this.collection.each(function(model){
                var item = new ArticleListItemView({
                    model: model,
                });
                container.append(item.render().el);
            });
            return this;
        }

    });

    return ArticleListView ;

});