# Sparta-project
 Bu readme'de Sparta Bilişim için istenile Case'in nasıl çalıştığını anlatacağım.

 # Frontend
 Frontend'de Bir value ve gönderdiğiniz verinin tipini girerek  fetch data tuşuna basarsanız .Data backend'e gider ve  burada eğer hostname ise  verinin tipi  dns enumaration işlemi yapılıp geri döner eğer değilse sadece gönderdiğimiz veriler, zaman ve tehlikeli olup olmadığı döner.

 Eğer diğer düğmeye basarsanız son 50 tane veriyi çekip size bir chart yapacaktır.

 # Backend
 Backend'de ise gelen veriyi  önce api kullanıp tehlikeli mi diye kontrol eder. Sonra bu veriyi firebase'de saklar.Ve bu işlemden sonra frontend bir daha fetch isteği yollar ve  yollanılan veri , zaman ve telikeli olup olmadığı döner. Bununla birlikte eğer diğer düğmeye basarsa kullanıcı , backend firebase'den son 50 datayı request edecektir. Bunları date'e göre sıralayacaktır. Ve sonra bunu frontendde json formatında yollayacaktır

