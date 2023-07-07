




!function ($) {

    "use strict";

    var Typed = function (el, options) {


        this.el = $(el);

        this.options = $.extend({}, $.fn.typed.defaults, options);


        this.text = this.el.text();


        this.typeSpeed = this.options.typeSpeed;


        this.backDelay = this.options.backDelay;


        this.strings = this.options.strings;

        this.strPos = 0;

        this.arrayPos = 0;


        this.string = this.strings[this.arrayPos];


        this.stopNum = 0;


        this.loop = this.options.loop;
        this.loopCount = this.options.loopCount;
        this.curLoop = 1;
        if (this.loop === false) {

            this.stopArray = this.strings.length - 1;
        }
        else {
            this.stopArray = this.strings.length;
        }

        this.init();
        this.build();
    }

    Typed.prototype = {

        constructor: Typed

        , init: function () {

            this.typewrite(this.string, this.strPos);
        }

        , build: function () {
            this.el.after("<span id=\"typed-cursor\">|</span>");
        }


        , typewrite: function (curString, curStrPos) {


            var humanize = Math.round(Math.random() * (100 - 30)) + this.typeSpeed;
            var self = this;

            setTimeout(function () {


                if (self.arrayPos < self.strings.length) {


                    self.el.text(self.text + curString.substr(0, curStrPos));

                    if (curStrPos > curString.length && self.arrayPos < self.stopArray) {
                        clearTimeout(clear);
                        var clear = setTimeout(function () {
                            self.backspace(curString, curStrPos);
                        }, self.backDelay);
                    }

                    else {

                        curStrPos++;

                        self.typewrite(curString, curStrPos);

                        if (self.loop === false) {
                            if (self.arrayPos === self.stopArray && curStrPos === curString.length) {

                                var clear = self.options.callback();
                                clearTimeout(clear);
                            }
                        }
                    }
                }

                else if (self.loop === true && self.loopCount === false) {
                    self.arrayPos = 0;
                    self.init();
                }
                else if (self.loopCount !== false && self.curLoop < self.loopCount) {
                    self.arrayPos = 0;
                    self.curLoop = self.curLoop + 1;
                    self.init();
                }


            }, humanize);

        }

        , backspace: function (curString, curStrPos) {

            var humanize = Math.round(Math.random() * (100 - 30)) + this.typeSpeed;
            var self = this;

            setTimeout(function () {

                if (self.arrayPos == 1, 2, 3, 4) {
                    self.stopNum = 0;
                }

                self.el.text(self.text + curString.substr(0, curStrPos));


                if (curStrPos > self.stopNum) {

                    curStrPos--;

                    self.backspace(curString, curStrPos);
                }

                else if (curStrPos <= self.stopNum) {
                    clearTimeout(clear);
                    var clear = self.arrayPos = self.arrayPos + 1;

                    self.typewrite(self.strings[self.arrayPos], curStrPos);
                }

            }, humanize);

        }

    }

    $.fn.typed = function (option) {
        return this.each(function () {
            var $this = $(this)
                , data = $this.data('typed')
                , options = typeof option == 'object' && option
            if (!data) $this.data('typed', (data = new Typed(this, options)))
            if (typeof option == 'string') data[option]()
        });
    }

    $.fn.typed.defaults = {
        strings: ["Hello, hola, hi! ", "Welcome to my website ", "Go on, scroll down", ":)"],

        typeSpeed: 50,

        backDelay: 100,
        loop: true,
        loopCount: false,
        callback: function () { null }
    }


}(window.jQuery);


$(function () {

    $("#typed").typed({
        strings: ["Welcome to my website", "I'm a JavaScript lover ❤️", "( ͡❛ ͜ʖ ͡❛)"],
        typeSpeed: 40,
        backDelay: 600,
        loop: true,
        loopCount: false,
        callback: function () { foo(); }
    });

    function foo() { console.log("Callback"); }

});










$(document).ready(function() { 
/*
===============================================================

Hi! Welcome to my little playground!

My name is Tobias Bogliolo. 'Open source' by default and always 'responsive',
I'm a publicist, visual designer and frontend developer based in Barcelona. 

Here you will find some of my personal experiments. Sometimes usefull,
sometimes simply for fun. You are free to use them for whatever you want 
but I would appreciate an attribution from my work. I hope you enjoy it.

===============================================================
*/

/*
=====================
=====================
JSON list
=====================
=====================
*/
var post=[
    {
      postTitle: "Lorem ipsum dolor",
      postAbstract: "Voluptates sit ducimus velit soluta ed doloribus iste commodi deserunt aut unde, numquam illo, unde.",
      postContent: "<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Debitis, molestiae placeat, inventore eligendi qui deserunt asperiores error laboriosam libero blanditiis dignissimos eius molestias cumque necessitatibus est. <b>Quae velit ad cupiditate necessitatibus</b>, facere eum earum ut odio nostrum labore a explicabo quasi voluptates, consequatur obcaecati quos, quis fugiat veniam ea ipsam consequuntur illo!</p><p>Aperiam fugit nulla, praesentium doloremque harum laborum ipsam officia minima. Alias saepe cumque mollitia soluta totam facere, iusto ab officiis cum itaque! Sit sint earum sequi quae mollitia quibusdam adipisci facere explicabo libero nihil! Velit aliquam asperiores possimus eligendi dolore reprehenderit similique suscipit.</p>",
      postThumb: "https://drive.google.com/uc?id=1XlEn94sZcbvOmeP3Ws5tWrrB3d8Qygc7",
      postImg: "https://drive.google.com/uc?id=12RhLJZygX4IJfcc5nFH_eJ4H2x_XuIuo",
      postLink: "article-link1"
    },
    {
      postTitle: "Sit amet consectetur",
      postAbstract: "Ipsum dolor sit amet, consectetur adipisicing elit. Quidem voluptatum, aliquam quaerat!",
      postContent: "<p>Porro, perferendis fugit nulla, praesentium doloremque harum laborum ipsam possimus. In, est optio fugiat itaque inventore suscipit voluptatem quam sit <b>voluptatibus nesciunt</b> quo, cum eius. Dolorem, animi, voluptas?</p><p>Necessitatibus esse tempore iure quasi molestias assumenda vitae, maxime corrupti aut blanditiis, odit facere ad tempora fugiat suscipit nulla consequatur, soluta. Dignissimos cupiditate assumenda voluptatum!</p>",
      postThumb: "https://drive.google.com/uc?id=14EiMBT5XfJsy6eKC3BfXNkiZGumbE_m4",
      postImg: "https://drive.google.com/uc?id=1EwgpldRKofLjlZ52BZNqsDiEVDw42Kb0",
      postLink: "article-link1"
    },
    {
      postTitle: "Adipisicing elit beatae",
      postAbstract: "Lorem ipsum dolor sit amet, odit nulla consectetur adipisicing elit. Fugit vero accusamus commodi ex?",
      postContent: "<p>Repudiandae voluptatem autem ab maiores <b>quaerat dicta illum</b> deleniti alias iure esse ex temporibus asperiores assumenda beatae veniam sit, eligendi magni quas quod, qui expedita similique error nulla debitis. Debitis <b>nemo ipsam rem dignissimos</b>, dicta repellat nulla nesciunt! Recusandae dicta numquam repellat tempore in cum, expedita. Quidem veniam, eos harum cumque aspernatur labore est enim voluptatibus numquam at ea vel provident facere doloremque. Natus, officiis eos!</p>",
      postThumb: "https://drive.google.com/uc?id=1-oDn7lhzEqaxMxo82q9yTqFWPxwg7K3S",
      postImg: "https://drive.google.com/uc?id=1YIh-6WX1zmZx44aSfv4chF1anCoIpRqV",
      postLink: "article-link1"
    },
    {
      postTitle: "Quidem neque commodi",
      postAbstract: "Aliquid sapiente harum maiores alias optio, ea vero perferendis impedit architecto culpa libero corporis.",
      postContent: "<p>Dolorum eos dignissimos eveniet deserunt veritatis possimus magnam enim, eaque non, architecto voluptates consequuntur nulla, modi nobis sunt perferendis voluptatibus accusantium voluptatem! Delectus iure architecto rem, ex quas necessitatibus illum autem obcaecati sapiente ea inventore quisquam debitis quae numquam. Iusto mollitia suscipit iste quae tempore ipsam facere <b>quia nobis et omnis accusantium quo</b>, quod tenetur, aperiam, rem quos quas eveniet exercitationem. Rem, hic optio. Harum quis porro optio facilis totam velit quibusdam corrupti saepe similique sed aut doloribus temporibus ipsum modi rerum, ab impedit.</p>",
      postThumb: "https://drive.google.com/uc?id=1e2xtcSexfjBxBFl4NPMHYZn65AfSo60w",
      postImg: "https://drive.google.com/uc?id=1W49XdIePB6K4QsiO5Nn6iXpneZ2MoiNG",
      postLink: "article-link1"
    },
    {
      postTitle: "Explicabo obcaecati",
      postAbstract: "Iste explicabo, architecto maiores nisi eaque doloribus aspernatur esse tera corporis iure itaque animi?",
      postContent: "<p>Voluptatem, similique. Sed doloribus quaerat ratione deleniti esse odit doloremque incidunt, aut, recusandae? Ipsam ipsum voluptas tenetur aut atque tempora ducimus, dolores qui, <b>maiores voluptatibus veniam</b>, quos inventore esse illum adipisci. Error quo officia, distinctio voluptates, possimus voluptatem dignissimos magni dolor, nobis expedita doloribus consequuntur beatae natus iusto ipsum culpa. Delectus pariatur, officia voluptatem, dolore enim cum temporibus deserunt reiciendis at quam labore aperiam, adipisci nesciunt.</p><p>Laborum placeat <b>adipisci ex porro</b>, labore impedit sed nulla perferendis architecto quis vitae laudantium animi, dolorum repudiandae incidunt eaque! Possimus corporis voluptatum aut velit similique facilis fugit quis eaque, fugiat inventore beatae minus nemo soluta quia earum, atque accusamus!</p>",
      postThumb: "https://drive.google.com/uc?id=1lDD2eMS-Kz8bn_4dv6VaUaVDwzSAH6q2",
      postImg: "https://drive.google.com/uc?id=1epjmOXGqRyriWfN1TSU0bB5xMEoFbr7X",
      postLink: "article-link1"
    },
    {
      postTitle: "Ullam provident",
      postAbstract: "Lorem ipsum dolor sit amet eveniet, consectetur adipisicing elit. Numquam repudiandae nam dolore.",
      postContent: "<p>Possimus ipsam, aliquid voluptate ab quaerat mollitia deleniti recusandae, voluptas quisquam consequatur porro nesciunt sed commodi reprehenderit, amet earum sapiente sunt, temporibus aut <b>consectetur eligendi</b> laudantium. Cum, eius! Optio tempora unde, non quasi fugit, eos corporis iusto dolores, quam suscipit ipsum cum nesciunt incidunt atque in recusandae amet totam ea fuga! Aliquid similique exercitationem accusamus, et vitae molestiae voluptatum quo earum doloribus <b>nisi hic nesciunt</b>, blanditiis dignissimos. Quia veniam neque facere nesciunt quibusdam distinctio architecto perferendis veritatis? Laboriosam architecto culpa hic aspernatur ratione possimus nostrum mollitia, soluta aliquid reiciendis doloribus.</p>",
      postThumb: "https://drive.google.com/uc?id=1-n-Z2x9dKpDKQe1gTLFunsO8Ok5Alasj",
      postImg: "https://drive.google.com/uc?id=1gH6RubwaKmWppZ42F0CRDXA0MlB3S8RF",
      postLink: "article-link1"
    }
  ];
  
  
  /*
  =====================
  =====================
  Thumbs
  =====================
  =====================
  */
  //Loop length:
  var postLength = post.length;
  //Empty container:
  $(".posts-box").empty();
  //Loop:
  for (i=0; i<postLength; i++) {
    //Create thumb structure:
    var listItem =
      '<li>'+
        '<div class="card">'+
          '<a class="button" href="'+post[i].postLink+'" data-obj="'+i+'">'+
            '<img src="'+post[i].postThumb+'" alt="">'+
          '</a>'+
          '<div>'+
            '<h3>'+post[i].postTitle+'</h3>'+
            '<p>'+post[i].postAbstract+'</p>'+
          '</div>'+
          '<div>'+
            '<a class="button" href="'+post[i].postLink+'" data-obj="'+i+'">Explore</a>'+
          '</div>'+
        '</div>'+
      '</li>';
    //Append thumb:
    $(".posts-box").append(listItem);
  };
  
  
  /*
  =====================
  =====================
  Inner post
  =====================
  =====================
  */
  var thisElement = 0;
  
  function innerContent(content){
    $(".inner-img").attr("src",post[content].postImg);
    $(".inner-title").html(post[content].postTitle);
    $(".inner-text").html(post[content].postContent);
  };
  
  //Open post:
  $(".button").click(function(e){
    e.preventDefault();
    thisElement = $(this).attr("data-obj");
    innerContent(thisElement);
    $(".modal").css({"display":"block"});
    dissBtn();
  });
  
  //Close post:
  $(".close-post, .modal-sandbox").click(function(){
    $(".modal").css({"display":"none"});
  });
  
  //Next post:
  $(".next-post").click(function(e){
    e.preventDefault();
    if (thisElement<postLength-1) {
      thisElement = parseInt(thisElement) + 1;
      innerContent(thisElement);
      dissBtn();
    };
  });
  
  //Prev post:
  $(".prev-post").click(function(e){
    e.preventDefault();
    if (thisElement>0) {
      thisElement = parseInt(thisElement) - 1;
      innerContent(thisElement);
      dissBtn();
    };
  });
  
  //Button disable:
  function dissBtn(){
    $(".prev-post, .next-post").removeClass("disabled");
    if (thisElement<=0){
      $(".prev-post").addClass("disabled");
    }
    else if (thisElement>=postLength-1){
      $(".next-post").addClass("disabled");
    };
  };
})