const hearts = document.querySelectorAll('.reaction-like')
var theLength = hearts.length
for (let i=0; i < theLength; i++){
    hearts[i].addEventListener('click', (el) => {
        var theImg = hearts[i].children[0]
        console.log(hearts[i].children)
        var action = theImg.dataset.action
        var pardiv = hearts[i]
        var postId = pardiv.dataset.postid
        console.log(pardiv, postId, action)
        $.post('/post/react',
                {
                    action: action,
                    post_id: postId
            },
            function(data){
                if(data['success'] == true){
                    var likes_count = hearts[i].parentElement.children[0]
                    var count = parseInt(likes_count.innerText)
                    if(action == 'like'){
                        var img = document.createElement('img')
                        img.src = '/static/heart.gif'
                        img.height = 37;
                        img.width = 37;
                        img.style.position = 'relative'
                        img.style.top = '-8px'
                        var el1 = hearts[i].children[0]
                        console.log(el1, 'el1')
                        hearts[i].replaceChild(img, el1)
                        // pardiv.append(img)
                        window.setTimeout(() => {
                        var img = document.createElement('img')
                            img.height = 37;
                            img.width = 37;
                            img.src = '/static/heart_40.png'
                            img.className = 'heart-gif'
                            img.setAttribute('data-action', 'unlike')
                            pardiv.replaceChild(img, hearts[i].children[0])
                            likes_count.innerText = count + 1
                        }, 480)
                    }
                    else if(action == 'unlike'){
                        var img = document.createElement('img')
                        img.src = '/static/new_test.gif'
                        img.height = 37;
                        img.width = 37;
                        img.style.position = 'relative'
                        img.style.top = '-8px'
                        var el1 = hearts[i].children[0]
                        console.log(el1, 'el1')
                        hearts[i].replaceChild(img, el1)
                        window.setTimeout(() => {
                            var img = document.createElement('img')
                            img.height = 37;
                            img.width = 37
                            img.src = '/static/download.png'
                            img.className = 'heart-gif'
                            img.setAttribute('data-action', 'like')
                            pardiv.replaceChild(img, hearts[i].children[0])
                                likes_count.innerText = count - 1
                        }, 250);
                    }
                }
            })      
        })
    }