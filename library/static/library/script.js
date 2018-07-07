

$( document ).ready(function() {
 bookdisplay = $(".bookdisplay");

 if (bookdisplay[0]){
     for(i=0;i<bookdisplay.length;i++){
       let isbn = bookdisplay.eq(i).data('isbn');

    console.log(isbn);

    $.ajax({
      dataType: 'json',
      url: 'https://www.googleapis.com/books/v1/volumes?q=isbn:'+ isbn,
      success: handleResponse
    });

    function handleResponse( response ) {
      $.each( response.items, function( i, item ) {


      let title    = item.volumeInfo.title,
          author   = item.volumeInfo.authors[0],
          thumb    = item.volumeInfo.imageLinks.thumbnail;

      $('.title').text( title );
      $('.author').text( author );
      $('.thumbnail').attr('src', thumb);
    });}
     }
  }

});