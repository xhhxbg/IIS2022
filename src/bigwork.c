#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

char country[0x28];

void backdoor()
{
	system("/bin/sh");
}

int menu()
{
	int choice;
	puts("Welcome to choose this chanllenge!!!");
	puts("Now, you have 3 choices:");
	puts("1.Overflow!");
	puts("2.Formatstring!");
	printf("Your choice: ");
	scanf("%d", &choice);
	return choice;
}

void overflow()
{
	char copy[0x28] = {};
	puts("Which country do you live in?");
	scanf("%s", copy);
	printf("Wow, %s is such a nice country!	\n", country);
	strcpy(country, copy);
	puts("It was nice meeting you. Goodbye!");
	return 0;
}

int main()
{
	char buf[0x30];
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);

	while (1)
	{
		switch (menu())
		{
		case 1:
			overflow();
			break;
		case 2:
			puts("What do you want to show?");
			memset(buf, 0, 0x60);
			read(0, buf, 0x60);
			printf("good!\n");
			printf(buf);
			break;
		}
	}

	return 0;
}
