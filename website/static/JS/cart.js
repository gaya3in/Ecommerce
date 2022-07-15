var updateBtns = document.getElementsByClassName('update-cart');

for(i=0;i<updateBtns.length;i++)
{
    updateBtns[i].addEventListener("click", function(){
      var productId = this.dataset.product
      var action = this.dataset.action
      console.log("ProductID: " ,productId, "Action: " ,action, "User:" ,user)

   if (user == "AnonymousUser"){
        addCookieItem(productId, action)
    }else{
       UpdateUserOrder(productId, action)
     }
  })
}

function addCookieItem(productId, action){
    if (action == "add")
    {
         if (cart[productId] == undefined)
        {
          cart[productId] = {'quantity': 1}
        }
        else
        {
          cart[productId]['quantity'] += 1
        }
    }

    if (action == "remove")
    {
       cart[productId]['quantity'] -= 1
       if (cart[productId]['quantity'] <= 0)
       {
         delete cart[productId]
       }
    }
    console.log(cart)
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain;path=/"
    location.reload()
}
function UpdateUserOrder(productId, action){
    var url = "/update_order/"

    fetch(url, {
      method: 'POST',
      headers: {
           'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
             },
      body: JSON.stringify({'productId' : productId, 'action': action})
      })

      .then(response =>{
        return response.json()
      })

      .catch(error =>{
         console.log(error)
      })

      .then((data) =>{
        console.log('data:' , data)
        location.reload()
      })


}
