
const questions = [
    {
       question:"Which is the largest animal in this world?",
       answers:[
        {text:"Shark", correct:false},
        {text:"Blue Whale", correct:true},
        {text:"Elephant", correct:false},
        {text:"Giraffe", correct:false},
       ]
    },
    {
       question:"Which is the largest animal in this world?",
       answers:[
        {text:"Shark", correct:false},
        {text:"Blue Whale", correct:true},
        {text:"Elephant", correct:false},
        {text:"Giraffe", correct:false},
       ]
    },
    {
       question:"Which is the largest desert in this world?",
       answers:[
        {text:"Kalahari", correct:false},
        {text:"Shara", correct:false},
        {text:"gobi", correct:false},
        {text:"antartica", correct:true},
       ]
    },
    {
       question:"Which is the smallest continent in this world?",
       answers:[
        {text:"Asia", correct:false},
        {text:"Australia", correct:true},
        {text:"Arctic", correct:false},
        {text:"Africa", correct:false},
       ]
    }
];

   const questionelement = document.getElementById("question");
   const answerbutton = document.getElementById("answer-buttons");
   const next = document.getElementById("next-btn");

   let currentindex = 0;
   let score = 0;

   function startquize(){
    currentindex = 0;
    score = 0;
    next.innerHTML="Next";
    showquestion();
   }

   function showquestion(){
    resetstate();
    let current = questions[currentindex];
    let questionNo = currentindex+1;
    questionelement.innerHTML=questionNo+". "+current.question;

    current.answers.forEach(answer=>{
        const button = document.createElement("button");
        button.innerHTML=answer.text;
        button.classList.add("btn");
        answerbutton.appendChild(button);
        
        if(answer.correct){
            button.dataset.correct=answer.correct;
        }
       button.addEventListener("click", selectAnswer);
    });
   }

   function resetstate(){
    next.style.display="none";
    while(answerbutton.firstChild){
        answerbutton.removeChild(answerbutton.firstChild);
    }
   }

   function selectAnswer(e){
    const selectbtn = e.target;
    const isCorrect = selectbtn.dataset.correct === "true";
    if(isCorrect){
        selectbtn.classList.add("correct");
        score++;
    }
    else{
        selectbtn.classList.add("incorrect")
    }

    Array.from(answerbutton.children).forEach(button=>{
        if(button.dataset.correct==="true"){
            button.classList.add("correct");
        }
        button.disabled=true;
    });
    next.style.display="block";
   }

   function showScore(){
     resetstate();
     questionelement.innerHTML=`Your Scored ${score} out of ${questions.length}!`;
     next.innerHTML="play again";
     next.style.display="block"
   }

   function handleNextButton(){
    currentindex++;
    if(currentindex<questions.length){
        showquestion();
    }else{
        showScore();
    }
   }



   next.addEventListener("click", ()=>{
         if(currentindex<questions.length){
            handleNextButton();
         }else{
            startquize();
         }
   })
   startquize();