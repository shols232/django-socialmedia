const hearts = document.querySelectorAll('.reaction-like')
var theLength = hearts.length
for (let i=0; i < theLength; i++){
    hearts[i].addEventListener('click', (el) => {
        var theImg = hearts[i].children[0]
        console.log(hearts[i].children)
        var action = theImg.dataset.action
        var react = theImg.dataset.react
        var pardiv = hearts[i]
        var postId = pardiv.dataset.postid
        console.log(pardiv, postId, action, react)
        $.post('/post/react',
                {
                    action: action,
                    post_id: postId,
                    react:react
            },
            function(data){
                if(data['success'] == true){
                    var likes_count = hearts[i].children[1]
                    var count = parseInt(likes_count.innerText)
                    var el1 = hearts[i].children[0]
                    if(action == 'like'){
                        var el1 = hearts[i].children[0]
                        if (react == 'love'){
                            var img = document.createElement('img')
                            img.src = '/static/heart.gif'
                            img.height = 19;
                            img.width = 19;
                            img.style.position = 'relative'
                            console.log(el1, 'el1')
                            hearts[i].replaceChild(img, el1)
                            window.setTimeout(() => {
                            var img = document.createElement('img')
                                img.height = 19;
                                img.width = 19;
                                img.src = '/static/heart_40.png'
                                img.className = 'heart-gif'
                                img.setAttribute('data-action', 'unlike')
                                img.setAttribute('data-react', 'love')
                                pardiv.replaceChild(img, hearts[i].children[0])
                                likes_count.innerText = count + 1
                            }, 480)
                        }else if(react == 'like'){
                            el1.style.color = '#5DA1D9'
                            el1.setAttribute('data-action', 'unlike')
                            likes_count.innerText = count + 1
                        }
                    }
                    else if(action == 'unlike'){
                        if (react == 'love'){
                            var img = document.createElement('img')
                            img.src = '/static/new_test.gif'
                            img.height = 19;
                            img.width = 19;
                            img.style.position = 'relative'
                            console.log(el1, 'el1')
                            hearts[i].replaceChild(img, el1)
                            window.setTimeout(() => {
                                var img = document.createElement('img')
                                img.height = 19;
                                img.width = 19
                                img.src = '/static/download.png'
                                img.className = 'heart-gif'
                                img.setAttribute('data-action', 'like')
                                img.setAttribute('data-react', 'love')
                                pardiv.replaceChild(img, hearts[i].children[0])
                                    likes_count.innerText = count - 1
                            }, 250);
                        }
                        else if(react == 'like'){
                            el1.style.color = '#8d8d8d'
                            el1.setAttribute('data-action', 'like')
                            likes_count.innerText = count - 1
                        }
                    }
                }
            })      
        })
    }