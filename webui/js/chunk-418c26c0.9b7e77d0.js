(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-418c26c0"],{1681:function(t,e,a){},1692:function(t,e,a){"use strict";a.r(e);var o=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-container",{staticClass:"mt-5"},[a("v-row",{attrs:{justify:"center","no-gutters":""}},[a("v-col",{attrs:{cols:"12",md:"10",lg:"10"}},[a("console")],1)],1),a("v-row",{staticStyle:{"margin-top":"-1px"},attrs:{justify:"center","no-gutters":""}},[a("v-col",{staticClass:"pt-0",attrs:{cols:"12",md:"10",lg:"10"}},[a("v-btn",{staticStyle:{"border-radius":"0px 0px 4px 4px"},attrs:{color:"error",disabled:!t.started,block:"",dense:"",outlined:""},on:{click:function(e){return t.$emit("stop")}}},[a("v-icon",{staticClass:"pt-0",attrs:{left:""}},[t._v(" mdi-stop-circle ")]),t._v(" Stop ")],1)],1)],1)],1)},n=[],s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-textarea",{staticStyle:{"font-family":"monospace, monospace","font-size":"1.1rem","border-radius":"4px 4px 0px 0px"},attrs:{value:t.log,"hide-details":!0,label:"Log",rows:"11",outlined:"","no-resize":"",readonly:""}})},r=[],i=(a("a15b"),{name:"Console",computed:{log:function(){return this.$store.state.gamestate.log.join("\n")||"You have no task in progress..."}}}),u=i,c=a("2877"),l=a("6544"),p=a.n(l),h=a("a844"),d=Object(c["a"])(u,s,r,!1,null,null,null),f=d.exports;p()(d,{VTextarea:h["a"]});var g={mounted:function(){this.ws.send(JSON.stringify({event:"req-current-state",msg:""}))},name:"Manager",components:{Console:f},props:{ws:WebSocket},computed:{log:function(){return this.$store.state.gamestate.log},started:function(){return this.$store.state.gamestate.started}}},m=g,w=a("8336"),v=a("62ad"),x=a("a523"),y=a("132d"),b=a("0fd9"),I=Object(c["a"])(m,o,n,!1,null,null,null);e["default"]=I.exports;p()(I,{VBtn:w["a"],VCol:v["a"],VContainer:x["a"],VIcon:y["a"],VRow:b["a"]})},a844:function(t,e,a){"use strict";a("a9e3");var o=a("5530"),n=(a("1681"),a("8654")),s=a("58df"),r=Object(s["a"])(n["a"]);e["a"]=r.extend({name:"v-textarea",props:{autoGrow:Boolean,noResize:Boolean,rowHeight:{type:[Number,String],default:24,validator:function(t){return!isNaN(parseFloat(t))}},rows:{type:[Number,String],default:5,validator:function(t){return!isNaN(parseInt(t,10))}}},computed:{classes:function(){return Object(o["a"])({"v-textarea":!0,"v-textarea--auto-grow":this.autoGrow,"v-textarea--no-resize":this.noResizeHandle},n["a"].options.computed.classes.call(this))},noResizeHandle:function(){return this.noResize||this.autoGrow}},watch:{lazyValue:function(){this.autoGrow&&this.$nextTick(this.calculateInputHeight)},rowHeight:function(){this.autoGrow&&this.$nextTick(this.calculateInputHeight)}},mounted:function(){var t=this;setTimeout((function(){t.autoGrow&&t.calculateInputHeight()}),0)},methods:{calculateInputHeight:function(){var t=this.$refs.input;if(t){t.style.height="0";var e=t.scrollHeight,a=parseInt(this.rows,10)*parseFloat(this.rowHeight);t.style.height=Math.max(a,e)+"px"}},genInput:function(){var t=n["a"].options.methods.genInput.call(this);return t.tag="textarea",delete t.data.attrs.type,t.data.attrs.rows=this.rows,t},onInput:function(t){n["a"].options.methods.onInput.call(this,t),this.autoGrow&&this.calculateInputHeight()},onKeyDown:function(t){this.isFocused&&13===t.keyCode&&t.stopPropagation(),this.$emit("keydown",t)}}})}}]);
//# sourceMappingURL=chunk-418c26c0.9b7e77d0.js.map