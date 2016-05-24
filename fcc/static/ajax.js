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
}


//For doing AJAX post

//When submit is clicked
 $("button#submitajax").click(function(e) {
//Prevent default submit. Must for Ajax post.Beginner's pit.
 e.preventDefault();

//Prepare csrf token
 var csrftoken = getCookie('csrftoken');

//Collect data from fields
 var titre = $('#id_titre').val();
 var message = $('#id_message').val();

//This is the Ajax post.Observe carefully. It is nothing but details of where_to_post,what_to_post
//Send data
 $.ajax({
       url : window.location.href, // the endpoint,commonly same url
       type : "POST", // http method
       data : { csrfmiddlewaretoken : csrftoken,
       titre : titre,
       message : message
 }, // data sent with the post request

 // handle a successful response
 success : function(json) {
 console.log(json); // another sanity check
 //On success show the data posted to server as a message
 $("#myModal").modal('hide');
 $("#news").load("/fcc/news");
 },

 // handle a non-successful response
 error : function(xhr,errmsg,err) {
 console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
 }
 });
});
