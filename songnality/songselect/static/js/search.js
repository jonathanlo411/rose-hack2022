
// Function to detect submission of search 
$('#id_search').keypress(function (e) {
    if (e.which == 13) {
        e.preventDefault();
        // serialize the data for sending the form data.
        var serializedData = $(this).serialize();
        // make POST ajax call
        $.ajax({
            type: 'POST',
            url: "post/ajax/searchsong",
            data: serializedData,
            success: function (response) {
                // get data from search and display

                alert("success!")
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    }
      return false; 
  });