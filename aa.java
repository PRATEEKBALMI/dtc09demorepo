//1. Write a program to display your information on the console.
import java.util.Scanner;

public class aa {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter your name: ");
        String name = scanner.nextLine();

        System.out.print("Enter your age: ");
        int age = scanner.nextInt();
        scanner.nextLine(); 

        System.out.print("Enter your favorite food: ");
        String favoriteFood = scanner.nextLine();

        System.out.println("\nUser Information:");
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
        System.out.println("Favorite Food: " + favoriteFood);

        scanner.close();
    }
}
