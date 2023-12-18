
    $(document).ready(function () {
        // Function to sort friends by name
        function sortFriendsByName() {
            $.get("{% url 'slambook:sort_friends' %}", function(data) {
                if (data.length > 0) {
                    var tableBody = $('#friends-table tbody');
                    tableBody.empty();
                    data.forEach(function(friend) {
                        var row = '<tr>' +
                            '<td>' + friend.name + '</td>' +
                            '<td><a href="#">' + friend.status + '</a></td>' +
                            '<td>' + friend.dateUpdated + '</td>' +
                            '</tr>';
                        tableBody.append(row);
                    });
                }
            });
        }

        // Handle the click event on the name column for sorting
        $('.friend-name').on('click', function() {
            sortFriendsByName();
        });
    });