function getCookie(name) {
          var cookieValue = null;
          if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
               var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
             }
          }
      }
 return cookieValue;
};

//Suppression d'une news
function suppNews(id_news) {
//Prepare csrf token
 var csrftoken = getCookie('csrftoken');

//Collect data from send parameter
 var id_news = id_news;

//This is the Ajax post.Observe carefully. It is nothing but details of where_to_post,what_to_post
//Send data
 $.ajax({
       url : '/fcc/supp_news', // the endpoint,commonly same url
       type : "POST", // http method
       data : { csrfmiddlewaretoken : csrftoken,
       id_news : id_news
 }, // data sent with the post request

 // handle a successful response
 success : function(json) {
 console.log(json); // another sanity check
 //On success show the data posted to server as a message
 $("#news").load("/fcc/news");
 },

 // handle a non-successful response
 error : function(xhr,errmsg,err) {
 console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
 }
 });
};


//Suppression d'un joker
function suppJoker(id_joker) {
//Prepare csrf token
 var csrftoken = getCookie('csrftoken');

//Collect data from send parameter
 var id_joker = id_joker;

//This is the Ajax post.Observe carefully. It is nothing but details of where_to_post,what_to_post
//Send data
 $.ajax({
       url : '/fcc/supp_joker', // the endpoint,commonly same url
       type : "POST", // http method
       data : { csrfmiddlewaretoken : csrftoken,
       id_joker : id_joker
 }, // data sent with the post request

 // handle a successful response
 success : function(json) {
 console.log(json); // another sanity check
 //On success show the data posted to server as a message
 $("#invites").load("/fcc/invites");
 },

 // handle a non-successful response
 error : function(xhr,errmsg,err) {
 console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
 }
 });
};
