/*
 * doctools.js
 * ~~~~~~~~~~~
 *
 * Sphinx JavaScript utilities for all documentation.
 *
 * :copyright: Copyright 2007-2011 by the Sphinx team, see AUTHORS.
 * :license: BSD, see LICENSE for details.
 *
 *//**
 * select a different prefix for underscore
 */$u=_.noConflict();jQuery.urldecode=function(e){return decodeURIComponent(e).replace(/\+/g," ")};jQuery.urlencode=encodeURIComponent;jQuery.getQueryParameters=function(e){typeof e=="undefined"&&(e=document.location.search);var t=e.substr(e.indexOf("?")+1).split("&"),n={};for(var r=0;r<t.length;r++){var i=t[r].split("=",2),s=jQuery.urldecode(i[0]),o=jQuery.urldecode(i[1]);s in n?n[s].push(o):n[s]=[o]}return n};jQuery.contains=function(e,t){for(var n=0;n<e.length;n++)if(e[n]==t)return!0;return!1};jQuery.fn.highlightText=function(e,t){function n(r){if(r.nodeType==3){var i=r.nodeValue,s=i.toLowerCase().indexOf(e);if(s>=0&&!jQuery(r.parentNode).hasClass(t)){var o=document.createElement("span");o.className=t;o.appendChild(document.createTextNode(i.substr(s,e.length)));r.parentNode.insertBefore(o,r.parentNode.insertBefore(document.createTextNode(i.substr(s+e.length)),r.nextSibling));r.nodeValue=i.substr(0,s)}}else jQuery(r).is("button, select, textarea")||jQuery.each(r.childNodes,function(){n(this)})}return this.each(function(){n(this)})};var Documentation={init:function(){this.fixFirefoxAnchorBug();this.highlightSearchWords();this.initIndexTable()},TRANSLATIONS:{},PLURAL_EXPR:function(e){return e==1?0:1},LOCALE:"unknown",gettext:function(e){var t=Documentation.TRANSLATIONS[e];return typeof t=="undefined"?e:typeof t=="string"?t:t[0]},ngettext:function(e,t,n){var r=Documentation.TRANSLATIONS[e];return typeof r=="undefined"?n==1?e:t:r[Documentation.PLURALEXPR(n)]},addTranslations:function(e){for(var t in e.messages)this.TRANSLATIONS[t]=e.messages[t];this.PLURAL_EXPR=new Function("n","return +("+e.plural_expr+")");this.LOCALE=e.locale},addContextElements:function(){$("div[id] > :header:first").each(function(){$('<a class="headerlink">¶</a>').attr("href","#"+this.id).attr("title",_("Permalink to this headline")).appendTo(this)});$("dt[id]").each(function(){$('<a class="headerlink">¶</a>').attr("href","#"+this.id).attr("title",_("Permalink to this definition")).appendTo(this)})},fixFirefoxAnchorBug:function(){document.location.hash&&$.browser.mozilla&&window.setTimeout(function(){document.location.href+=""},10)},highlightSearchWords:function(){var e=$.getQueryParameters(),t=e.highlight?e.highlight[0].split(/\s+/):[];if(t.length){var n=$("div.body");window.setTimeout(function(){$.each(t,function(){n.highlightText(this.toLowerCase(),"highlighted")})},10);$('<p class="highlight-link"><a href="javascript:Documentation.hideSearchWords()">'+_("Hide Search Matches")+"</a></p>").appendTo($("#searchbox"))}},initIndexTable:function(){var e=$("img.toggler").click(function(){var e=$(this).attr("src"),t=$(this).attr("id").substr(7);$("tr.cg-"+t).toggle();e.substr(-9)=="minus.png"?$(this).attr("src",e.substr(0,e.length-9)+"plus.png"):$(this).attr("src",e.substr(0,e.length-8)+"minus.png")}).css("display","");DOCUMENTATION_OPTIONS.COLLAPSE_INDEX&&e.click()},hideSearchWords:function(){$("#searchbox .highlight-link").fadeOut(300);$("span.highlighted").removeClass("highlighted")},makeURL:function(e){return DOCUMENTATION_OPTIONS.URL_ROOT+"/"+e},getCurrentURL:function(){var e=document.location.pathname,t=e.split(/\//);$.each(DOCUMENTATION_OPTIONS.URL_ROOT.split(/\//),function(){this==".."&&t.pop()});var n=t.join("/");return e.substring(n.lastIndexOf("/")+1,e.length-1)}};_=Documentation.gettext;$(document).ready(function(){Documentation.init()});