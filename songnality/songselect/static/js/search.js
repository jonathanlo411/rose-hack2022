$( document ).ready(function() {
    $('#search-bar').keypress(function (e) {
        if (e.key === "Enter") {
            var searchVal = $('#search-bar').val()
            $.ajax({
                type: 'POST',
                url: "/post/ajax/searchsong",
                data: {
                    "search": searchVal,
                    "sp": '{{ sp }}'
                },
                success: function (response) {
                    // get data from search and display
                    $('.search-results').css("display", "inline")
                    $('#spotify').css("margin-top", "3vh")
                    console.log(response)
                },
                error: function (response) {
                    // alert the error if any error occured
                    alert("failure alert");
                }
            })
        }
    });
  });

