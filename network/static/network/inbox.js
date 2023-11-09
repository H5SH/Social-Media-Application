

document.addEventListener('DOMContentLoaded', ()=> {
    document.querySelector('#allpost').addEventListener('click', ()=> mainpage());
    try{
        document.querySelector('#newpost_form').addEventListener('submit', () => newpost());
        document.querySelector('#user').addEventListener('click', ()=> profile(document.querySelector('#username').value));
    }
    catch(err){

    }
    

    mainpage();
})

function profile(username)
{
    try{
        document.querySelector('#div_newpost').style.display = 'none';
        document.querySelector('#singlepost').style.display = 'none';
        // if profile exccess from a post then display user's post in allpost
        // so unblocking it which was previously blocked in single post display
        document.querySelector('#div_allpost').style.display = 'block';
        document.querySelector('#div_allpost').innerHTML = '';
        document.querySelector('#profile_div').style.display = 'block';
        document.querySelector('#profile_div').innerHTML = ' ';
    }
    catch(err){

    }

    const current_user = document.querySelector('#username').value;
    fetch(`/user/${username}/${current_user}`)
    .then(response => response.json())
    .then(user => {
        const h1 = document.createElement('h1');
        h1.id = 'profile';
        h1.innerHTML = username;
        const table = document.createElement('table');
        table.innerHTML = `<tr><th>Followings</th><th>Followers</th></tr><tr><td>${user['followings']}</td><td>${user['followers']}</td></tr>`;
        displayposts(user['post']);
        document.querySelector('#profile_div').append(h1);
        document.querySelector('#profile_div').append(table);
        if (current_user != username)
        {
            const follow = document.createElement('button');
            if (user['follow'] === 'followed')
            {
                follow.id = 'notfollowed';
                follow.innerHTML = 'Unfollow';
            }
            else{
                follow.innerHTML = 'Follow';
                follow.id = 'followed';
            }
            document.querySelector('#profile_div').append(follow);
            // follow button onclick
            follow.addEventListener('click', ()=> {
                //user is unfollowing the id
                if (follow.id === 'followed')
                {
                    follow.id = 'notfollowed';
                    follow.innerHTML = 'Unfollow';
                    fetch(`/following/${username}`,{
                        method: 'PUT',
                        body: JSON.stringify({
                            follow: 'followed'
                        })
                        
                    })
                    .then(response => response.json())
                    .then(result => {
                        user['followers'] = result;
                    })
                    .catch(error => {
                        console.log(error);
                    });
                }
                // else the user is following
                else{
                    follow.id = 'followed';
                    follow.innerHTML = 'follow';
                    fetch(`/following/${username}`,{
                        method: 'PUT',
                        body: JSON.stringify({
                            follow: 'unfollowed'
                        })
                    })
                    .then(response => response.json())
                    .then(result => {
                        user['followings'] = result;
                    })
                    .catch(error => {
                        console.log(error);
                    })
                }
            })
        }
        
    })
}

function newpost()
{
    
    fetch('/allpost',{
        method: 'POST',
        body: JSON.stringify({
            post: document.querySelector('#newpost_text').innerHTML
        })
    })
    .then(response => response.json())
    .then(posts => {
        // clearing the allpost to display them again
        console.log(posts);
        document.querySelector('#div_allpost').innerHTML = '';
        displayposts(posts);
    })
    .catch(error => {
        console.log(error);
    });
}

    // fetch('/emails', {
    //     method: 'POST',
    //     body: JSON.stringify({
    //         recipients: 'baz@example.com',
    //         subject: 'Meeting time',
    //         body: 'How about we meet tomorrow at 3pm?'
    //     })
    //   })
    //   .then(response => response.json())
    //   .then(result => {
    //       // Print result
    //       console.log(result);
    //   });



function mainpage()
{
    document.querySelector('#div_allpost').innerHTML = '';
    document.querySelector('#profile_div').style.display = 'none';
    document.querySelector('#singlepost').style.display = 'none';
    fetch('/allpost')
    .then(response => response.json())
    .then(posts => {
        console.log(posts);
        displayposts(posts);
    })
    .catch(error => {
        console.log(error);
    });
}

function displayposts(posts)
{
    posts.forEach(element => {
        const div = document.createElement('div');
        const a = document.createElement('a');
        div.className = 'displaypost';
        div.innerHTML = `<h6>${element.username}</h6><p>${element.body}</p><p>${element.likes}</p>${element.time}`;
        a.append(div);
        document.querySelector('#div_allpost').append(a);

        // display single post
        div.addEventListener('click', ()=> {
            try{
                document.querySelector('#div_allpost').style.display = 'none';
                document.querySelector('#div_newpost').style.display = 'none';
                document.querySelector('#profile_div').style.display = 'none';
            }
            catch(err){

            }
            
            document.querySelector('#singlepost').style.display = 'block';
            document.querySelector('#singlepost').innerHTML = ' ';
            const div = document.querySelector('#singlepost');
            const p = document.createElement('p');
            const h3 = document.createElement('h3');
            const like_button = document.createElement('button');

            like_button.className = 'fa fa-thumbs-up';
            p.innerHTML = `${element.body}<br>${element.time}`;

            h3.innerHTML = `${element.username}`;
            h3.className = 'username';
            h3.addEventListener('click', ()=> profile(h3.innerHTML));

            // to see if the user has previously liked the post or not
            const username = document.querySelector('#username').value;
            fetch(`/likes/${element.id}/${username}`)
            .then(response => response.json())
            .then(like => {
                like_button.id = like;
                if (like === 'liked')
                {
                    like_button.innerHTML = `Unlike${element.likes}`
                }
                else{
                    like_button.innerHTML = `Like${element.likes}`
                }
            })
            .catch(error => {
                console.log(error);
            });
            div.append(h3);
            div.append(p);
            if (username != 'guest')
                div.append(like_button);    

            like_button.addEventListener('click', ()=> {
                if (like_button.id === 'liked')
                {
                    like_button.id = 'notliked';
                    fetch(`/likes/${element.id}/${username}`,{
                        method: 'PUT',
                        body: JSON.stringify({
                            likes: 'Unliked'
                        })
                    })
                    .then(response => response.json())
                    .then(likes => {
                        like_button.innerHTML = `Like${likes}`;
                    })
                    .catch(error => {
                        console.log(error);
                    });
                }
                else{
                    like_button.id = 'liked';
                    fetch(`/likes/${element.id}/${username}`,{
                        method: 'PUT',
                        body: JSON.stringify({
                            likes: 'liked'
                        })
                    })
                    .then(response => response.json())
                    .then(likes => {
                        like_button.innerHTML = `Dislike${likes}`;
                    })
                    .catch(error=> {
                        console.log(error);
                    });
                }
            })
            
        })
        
    });
}