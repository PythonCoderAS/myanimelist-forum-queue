const postsPending = [];

function updateNewPosts(){
    if (postsPending.length > 0) {
        fetch("/api/updated_posts", {
            method: "POST",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: {
                posts: postsPending
            }
        }).then((response) => {
            return response.json()
        }).then((/** @type {{submitted?: {id: number, html: string}[]}} */ data) => {
            const submitted = data.submitted || [];
            submitted.forEach((post) => {
                const postElement = document.getElementById(`post-${post.id}`);
                if (postElement) {
                    postElement.innerHTML = post.html;
                }
                postsPending.splice(postsPending.indexOf(post.id), 1);
            });
        })
    }
}

setInterval(updateNewPosts, 5000);
