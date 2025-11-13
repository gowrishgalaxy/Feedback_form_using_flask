document.addEventListener('DOMContentLoaded', function() {
    // --- (Your existing form validation logic can remain) ---
    const feedbackForm = document.getElementById('feedbackForm');
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function(event) {
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const message = document.getElementById('message').value.trim();

            if (name === '' || email === '' || message === '') {
                alert('Please fill out all fields.');
                event.preventDefault();
            }
        });
    }

    // Handle the "Accept All" button click
    const acceptAllBtn = document.getElementById('acceptAllBtn');
    if (acceptAllBtn) {
        acceptAllBtn.addEventListener('click', function() { [2, 5]
            if (confirm('Are you sure you want to accept all pending feedback?')) {
                fetch('/accept-all', {
                    method: 'POST',
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        alert(data.message);
                        // Reload the page to show the updated status
                        window.location.reload();
                    } else {
                        alert('Error: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while accepting feedback.');
                });
            }
        });
    }
});
