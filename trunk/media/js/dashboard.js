
var iDashboard = {
    
    jQuery : $,
    
    settings : {
        columns : '.column',
        gadgetSelector: '.gadget',
        handleSelector: '.gadget-head',
        contentSelector: '.gadget-content',
        dashboardName: 'NA',
        fields: [],
        
        
        gadgetDefault : {
            movable: true,
            removable: true,
            collapsible: true,
            editable: true,
            colorClasses : ['color-yellow', 'color-red', 'color-blue', 'color-white', 'color-orange', 'color-green', 'color-purple']
        },
        gadgetIndividual : function (id) {
            return mainGadgetIndividual(id);
           
        }
    },

    init : function (name) {
        this.attachStylesheet('/media/css/dashboard.js.css');
        this.sortGadgets();
        this.addGadgetControls();
        this.makeSortable();
        this.settings.dashboardName=name;
    },
    
    getGadgetSettings : function (id) {
        var $ = this.jQuery,
            settings = this.settings;
            var gi = settings.gadgetIndividual(id);
        return (id && gi) ? $.extend({},settings.gadgetDefault,gi) : settings.gadgetDefault;
    },
    
    addGadgetControls : function () {
        var iDashboard = this,
            $ = this.jQuery,
            settings = this.settings;
            
        $(settings.gadgetSelector, $(settings.columns)).each(function () {
            var thisGadgetSettings = iDashboard.getGadgetSettings(this.id);
            if (thisGadgetSettings.removable) {
                $('<a href="#" class="remove">CLOSE</a>').mousedown(function (e) {
                    /* STOP event bubbling */
                    e.stopPropagation();    
                }).click(function () {
                    if(confirm('This gadget will be removed, ok?')) {
                        $(this).parents(settings.gadgetSelector).animate({
                            opacity: 0    
                        },function () {
                            $(this).wrap('<div/>').parent().slideUp(function () {
                                $(this).remove();
                                iDashboard.savePreferences();
                            });
                        });
                    }
                    return false;
                }).appendTo($(settings.handleSelector, this));
            }
            
            if (thisGadgetSettings.editable) {
                $('<a href="#" class="edit">EDIT</a>').mousedown(function (e) {
                    /* STOP event bubbling */
                    e.stopPropagation();    
                }).toggle(function () {
                    $(this).css({backgroundPosition: '-66px 0', width: '55px'})
                        .parents(settings.gadgetSelector)
                            .find('.edit-box').show().find('input').focus();
                    return false;
                },function () {
                    $(this).css({backgroundPosition: '', width: '24px'})
                        .parents(settings.gadgetSelector)
                            .find('.edit-box').hide();
                    return false;
                }).appendTo($(settings.handleSelector,this));
                $('<div class="edit-box" style="display:none;"/>')
                    .append('<ul><li class="item"><label>Change the title?</label><input name="gadgettitle" value="' + $('h3',this).text() + '"/></li>')
                    .append((function(){
                        var colorList = '<li class="item"><label>Available colours:</label><ul class="colors">';
                        $(thisGadgetSettings.colorClasses).each(function () {
                            colorList += '<li class="' + this + '"/>';
                        });
                        return colorList + '</ul>';
                    })())
                    .append((function(){
                        fieldList = '';
                        $(thisGadgetSettings.fields).each(function () {
                            if (this.type == 'text') {
                                fieldList += '<ul><li class="item"><label>'+this.title+'</label><input name="'+this.id+'" value="'+this.value+'"/></li>';
                            } else if(this.type == 'choice') {
                                fieldList += '<ul><li class="item"><label>'+this.title+'</label><select name="'+this.id+'">';
                                selected = this.value;
                                $(this.choices).each(function () {
                                    if (this == selected) {
                                        fieldList += '<option selected>'+this+'</option>';
                                    } else {
                                        fieldList += '<option>'+this+'</option>';
                                    }
                                });
                                fieldList += '</select></li>';
                            }
                        });
                        return fieldList;
                    })())
                    .append('</ul>')
                    .insertAfter($(settings.handleSelector,this));
                    
            }
            
            if (thisGadgetSettings.collapsible) {
                $('<a href="#" class="collapse">COLLAPSE</a>').mousedown(function (e) {
                    /* STOP event bubbling */
                    e.stopPropagation();    
                }).click(function(){
                    $(this).parents(settings.gadgetSelector).toggleClass('collapsed');
                    iDashboard.savePreferences();
                    return false;    
                }).prependTo($(settings.handleSelector,this));
            }
        });
        
        $('.edit-box').each(function () {
            $('input',this).keyup(function () {
                if (this.name == 'gadgettitle') {
                    $(this).parents(settings.gadgetSelector).find('h3').text( $(this).val().length>20 ? $(this).val().substr(0,20)+'...' : $(this).val() );
                }

                iDashboard.savePreferences();
            });
            $('ul.colors li',this).click(function () {
                
                var colorStylePattern = /\bcolor-[\w]{1,}\b/,
                    thisGadgetColorClass = $(this).parents(settings.gadgetSelector).attr('class').match(colorStylePattern)
                if (thisGadgetColorClass) {
                    $(this).parents(settings.gadgetSelector)
                        .removeClass(thisGadgetColorClass[0])
                        .addClass($(this).attr('class').match(colorStylePattern)[0]);
                    iDashboard.savePreferences();
                }
                return false;
                
            });
        });
        
    },
    
    attachStylesheet : function (href) {
        var $ = this.jQuery;
        return $('<link href="' + href + '" rel="stylesheet" type="text/css" />').appendTo('head');
    },
    
    makeSortable : function () {
        var iDashboard = this,
            $ = this.jQuery,
            settings = this.settings,
            $sortableItems = (function () {
                var notSortable = '';
                $(settings.gadgetSelector,$(settings.columns)).each(function (i) {
                    if (!iDashboard.getGadgetSettings(this.id).movable) {
                        if(!this.id) {
                            this.id = 'gadget-no-id-' + i;
                        }
                        notSortable += '#' + this.id + ',';
                    }
                });
                return $('> li:not(' + notSortable + ')', settings.columns);
            })();
        
        $sortableItems.find(settings.handleSelector).css({
            cursor: 'move'
        }).mousedown(function (e) {
            $sortableItems.css({width:''});
            $(this).parent().css({
                width: $(this).parent().width() + 'px'
            });
        }).mouseup(function () {
            if(!$(this).parent().hasClass('dragging')) {
                $(this).parent().css({width:''});
            } else {
                $(settings.columns).sortable('disable');
            }
        });

        $(settings.columns).sortable({
            items: $sortableItems,
            connectWith: $(settings.columns),
            handle: settings.handleSelector,
            placeholder: 'gadget-placeholder',
            forcePlaceholderSize: true,
            revert: 300,
            delay: 100,
            opacity: 0.8,
            containment: 'document',
            start: function (e,ui) {
                $(ui.helper).addClass('dragging');
            },
            stop: function (e,ui) {
                $(ui.item).css({width:''}).removeClass('dragging');
                $(settings.columns).sortable('enable');
                iDashboard.savePreferences();
            }
        });
    },
    
    savePreferences : function () {
        var iDashboard = this,
            $ = this.jQuery,
            settings = this.settings,
        xml_string="<xml>\r\n";
        $(settings.columns).each(function(i){
            column_number = i+1;
            xml_string+="<column id=\""+column_number+"\">\r\n";
            $(settings.gadgetSelector,this).each(function(i){
                collapse=$(settings.contentSelector,this).css('display') == 'none' ? "true" : "false";
                xml_string+="<gadget id=\""+$(this).attr('dbid')+"\" \
colour=\""+$(this).attr('class').match(/\bcolor-[\w]{1,}\b/)+"\" \
title=\""+$('h3:eq(0)',this).text().replace(/\|/g,'[-PIPE-]').replace(/,/g,'[-COMMA-]')+"\" \
collapsed=\""+collapse+"\"/> \r\n";
            });
            xml_string+="</column>\r\n";
        });
        
        xml_string+="</xml>\r\n";
        $.post("/dashboard/update-ajax/"+this.settings.dashboardName+"/", { xml: xml_string },function(data){});
        
    },
    
    sortGadgets : function () {
        var iDashboard = this,
            $ = this.jQuery,
            settings = this.settings;
        
        $(settings.columns).each(function(i){
        //alert('load here');
        });
                
        $('body').css({background:'#000'});
        $(settings.columns).css({visibility:'visible'});
    }
  
};

