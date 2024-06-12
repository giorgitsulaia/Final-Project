მოცემული ფინალური პროექტი ეხება სტარტაპს სახელწოდებით - Rage Room Tbilisi. შევქმენი აპლიკაცია, რომელიც მომხმარებელს საშუალებას აძლევს უფრო მარტივად და სწაფად ისარგებლოს Rage Room Tbilisi-ის მომსახურებით.
კოდის გაშვების შემდეგ, მომხმარებელს აქვს საშუალება გააკეთოს რამდენიმე არჩევანი. კერძოდ მომხმარებელს:
  1) შეუძლია ნახოს პაკეტები (თითოეულის დასახელება, ფასი და მასში შემავალი ნივთები და მათი რაოდენობა)
  2) შეუძლია შექმნას ანგარიში
  3) შეუძლია შევიდეს მის მიერ უკვე შექმნილ ანგარიშში
  4) გამოვიდეს პროგრამიდან

მას შემდეგ, რაც მომხმარებელი გაივლის რეგისტრაციას ან შევა მის ანგარიშში (სადაც ხდება ყველა მონაცემის ვალიდაცია), მომხმარებელს აქვს საშუალება ნახოს ახალი მენიუ, საიდანაც მას უკვე დაჯავშნა შეუძლია. ეს მენიუ მოიცავს შემდეგს:
  1) Rage Room Tbilisi-ის ზოგადი განრიგის ჩვენება (1 კვირის მანძილზე)
  2) ბალანსზე თანხის შეტანა
  3) ოთახის კონკრეტულ დღეს, კონკრეტულ საათზე სასურველი პაკეტ(ებ)ის დაჯავშნა 
  4) საკუთარი ჯავშნის/ჯავშნების შესახებ ინფორმაციის ნახვა: თარიღი, საათი და პაკეტ(ებ)ი
  5) საკუთარი ჯავშნის გაუქმება
  6) საკუთარი ანგარიშიდან გამოსვლა და დაბრუნება საწყის მენიუზე

პროგრამისთვის კიდევ უფრო მეტი ინტერესის მისაცემად, "მფლობელისთვის" შევიმუშავე შემდეგი ლოგიკა, რომელსაც შესაძლებლობა ექნება ნახოს სტატისტიკა -->
--> ყველაზე ხშირად დაჯავშნად პაკეტზე, ყველაზე მეტად მოთხოვნად კვირის დღეზე, მომხმარებელთა საშუალო ასაკზე, ყველაზე მეტად რა ასაკის მომხმარებლები ჰყავს კომპანიას და ინფორმაცია მიმდინარე ჯავშნებზე.

მთავარი მენიუდან ანგარიშის შეყვანის ველში, "საიდუმლოდ" შექმნილი username-თი და პაროლით, "მფლობელს" წვდომა ეძლევა სტარტაპის სტატისტიკაზე.
"მფლობელის" ანგარიში შედგება:  username = owner, password = owner123

მას შემდეგ რაც ამ ანგარიშის "მფლობელი" შევა სისტემაში, ნახავს შემდეგ მენიუს:
  1) სტატისტიკის ნახვა
  2) ანგარიშიდან გამოსვლა
  3) პროგრამიდან გამოსვლა

კოდის წერისას ვეცადე ყველანაირ პოტენციურ error-ს გავმკლავებოდი. ასევე ვმუშაობ ორი ტიპის ფაილთან: json და ექსელის (.xlsx). ვიყენებ OOP-ს აპლიკაციის კონცეფციის შესაბამისად. ვიყენებ pandas ბიბლიოთეკას და აქამდე ნასწავლ თითქმის ყველა მასალას.

წინასწარ გიხდით მადლობას დროის დათმობისთვის და იმედია ამ კოდით ისიამოვნებთ :)

