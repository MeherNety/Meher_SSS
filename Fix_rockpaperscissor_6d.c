#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

void play(int *score){
	char computer_selection;
	char dummy_flag[2] = {'c','l'};
	char user_selection;
	char choices[3] = {'R','P','S'};
	int won = 0;
	computer_selection = choices[rand() % 3];

	printf("Choose (R)ock,(P)aper, or (S)cissor: ");
	scanf(" %1s",&user_selection);
	
	user_selection = toupper(user_selection);
	
	printf("You: %c - Computer: %c\n",user_selection,computer_selection);
	if(user_selection != computer_selection){
		if(user_selection == 'R' 
		   && computer_selection =='P'){
			won = 1;		
		}

		if(user_selection == 'P'
		   && computer_selection == 'R'){
			won = 1;
		}

		if(user_selection == 'S'
		  && computer_selection == 'P'){
			won = 1;
		}
	}
	if(won){
		score++;
		printf("\t+ You won!\n");
	}else{
		printf("\t- You lost!\n");
	}
}


int main(){
	int played = 0;
	char input = 'c';
	int win = 0;
	while(1){
		printf("Press P to play,E for scores, or X to exit: ");
		scanf(" %c",&input);
		input = toupper(input);
		if(input == 'X'){
			break;
		}
		else if(input =='P'){
			played++;
			play(&win);
		}
		else if(input =='E'){
			printf("\twon:%d\n\tplayed:%d\n",win,played);
		}
		else{
			printf("Invalid input!\n");
		}
	}
	return 0;
}
