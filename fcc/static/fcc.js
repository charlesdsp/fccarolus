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

//Suppression d'une news
function suppNews(id_news) {
var id_news = id_news;
//Demande une confirmation de suppression
if (!$('#dataConfirmModal').length) {
    $('body').append('<div id="dataConfirmModal" class="modal" role="dialog" aria-labelledby="dataConfirmLabel" aria-hidden="true"><div class="modal-dialog modal-sm"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>Confirmation suppression</div><div class="modal-footer"><button class="btn btn-sm" data-dismiss="modal" aria-hidden="true">Annuler</button><a class="btn btn-sm btn-danger" id="dataConfirmOK">Oui</a></div></div></div></div>');
}
$('#dataConfirmModal').modal({show:true});
$('#dataConfirmOK').click(function(e) {
//Prevent default submit. Must for Ajax post.Beginner's pit.
e.preventDefault();

    //Prepare csrf token
     var csrftoken = getCookie('csrftoken');

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
     $("#dataConfirmModal").modal('hide');
     $("#news").load("/fcc/news");
     },

     // handle a non-successful response
     error : function(xhr,errmsg,err) {
     console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
     }
     });
 });
};




function confirmSupp() {
	var href = $(this).attr('href');

	if (!$('#dataConfirmModal').length) {
		$('body').append('<div id="dataConfirmModal" class="modal" role="dialog" aria-labelledby="dataConfirmLabel" aria-hidden="true"><div class="modal-dialog modal-sm"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>Confirmation suppression</div><div class="modal-footer"><button class="btn btn-sm" data-dismiss="modal" aria-hidden="true">Annuler</button><a class="btn btn-sm btn-danger" id="dataConfirmOK">Oui</a></div></div></div></div>');
	}
    $('#dataConfirmModal').modal({show:true});
    $('#dataConfirmOK').click(function(e) {
   //Prevent default submit. Must for Ajax post.Beginner's pit.
    e.preventDefault();
    $("#dataConfirmModal").modal('hide');
    return true;
    });


	return false;
};
