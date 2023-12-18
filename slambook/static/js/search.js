$(document).ready(function() {
    // // upon clicking on search button
    // $('form.friends-search').submit(function (event) {
    //     event.preventDefault();
    //     var searchterm = $('form.friends-search input#friends-search-box').val();
    //     if (searchterm === "") {
    //         var message = $('<p class="search-error-message">Please enter a search term</p>');
    //         //appending error message
    //         $(message).appendTo($(this)).fadeOut(5000, function () {
    //             $(this).remove();
    //         });
    //     } else if (searchterm == "Mariah") {
    //         var message = $('<p class="search-success-message">Found search results!</p>');
    //         //appending success message
    //         $(message).appendTo($(this)).fadeOut(5000, function () {
    //             $(this).remove();
    //         });
    //         var allrows = $('div.friends-table table tbody').html();
    //         var searchresult = $('div.friends-table table tbody tr:contains(Mariah)');
    //         //replacing table data with search result
    //         $('div.friends-table table tbody').html(searchresult);
    //
    //         var clearresults = $('<button class="clear-results">Clear Results</button>');
    //         $(clearresults).appendTo($(this));
    //         console.log(allrows);
    //         //upon clicking on clear results button
    //         $(clearresults).click(function () {
    //             $('div.friends-table table tbody').html(allrows);
    //             $(clearresults).remove();
    //             $('form.friends-search input#friends-search-box').val("");
    //         });
    //     } else {
    //         var message = $('<p class="search-error-message">No search results found!</p>');
    //         //appending error message
    //         $(message).appendTo($(this)).fadeOut(5000, function () {
    //             $(this).remove();
    //         });
    //     }
    // });
  // upon clicking on search button
    $('form.friends-search').submit(function (event) {
        event.preventDefault();
        var searchterm = $('form.friends-search input#friends-search-box').val();

        if (searchterm === "") {
            var message = $('<p class="search-error-message">Please enter a search term</p>');
            // appending error message
            $(message).appendTo($(this)).fadeOut(5000, function () {
                $(this).remove();
            });
        } else {
            // Perform an AJAX request to the server to search for friends
            $.ajax({
                type: 'GET',
                url: '{% url "slambook:search-friends" %}',  // Replace with the actual URL to your search endpoint
                data: { searchterm: searchterm },
                success: function(data) {
                    if (data.length > 0) {
                        var message = $('<p class="search-success-message">Found search results!</p>');
                        // appending success message
                        $(message).appendTo($('form.friends-search')).fadeOut(5000, function () {
                            $(this).remove();
                        });

                        var allrows = $('div.friends-table table tbody').html();
                        var searchresult = data;  // Assuming the server returns the search results as HTML or a JSON array

                        // replacing table data with search result
                        $('div.friends-table table tbody').html(searchresult);

                        var clearresults = $('<button class="clear-results">Clear Results</button>');
                        $(clearresults).appendTo($('form.friends-search'));

                        // upon clicking on clear results button
                        $(clearresults).click(function () {
                            $('div.friends-table table tbody').html(allrows);
                            $(clearresults).remove();
                            $('form.friends-search input#friends-search-box').val("");
                        });
                    } else {
                        var message = $('<p class="search-error-message">No search results found!</p>');
                        // appending error message
                        $(message).appendTo($('form.friends-search')).fadeOut(5000, function () {
                            $(this).remove();
                        });
                    }
                },
                error: function() {
                    // Handle AJAX error
                }
            });
        }
    });
});