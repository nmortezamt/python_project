# disply hands
import cv2
import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 8: 
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

using System;
using System.Collections.Generic;
using System.IO;

class ProductManagement
{
    static string filePath = "products.txt";

    static void Main(string[] args)
    {
        List<string> products = LoadProducts();
        int choice = 0;

        do
        {
            Console.WriteLine("\nProduct Management System:");
            Console.WriteLine("1. Add Product");
            Console.WriteLine("2. Edit Product");
            Console.WriteLine("3. Show Products");
            Console.WriteLine("4. Exit");
            Console.Write("Enter your choice: ");
            
            if (int.TryParse(Console.ReadLine(), out choice))
            {
                switch (choice)
                {
                    case 1:
                        AddProduct(products);
                        break;
                    case 2:
                        EditProduct(products);
                        break;
                    case 3:
                        ShowProducts(products);
                        break;
                    case 4:
                        SaveProducts(products);
                        Console.WriteLine("Exiting...");
                        break;
                    default:
                        Console.WriteLine("Invalid choice! Please select again.");
                        break;
                }
            }
        } while (choice != 4);
    }

    // Load products from file
    static List<string> LoadProducts()
    {
        if (!File.Exists(filePath))
        {
            return new List<string>();
        }

        return new List<string>(File.ReadAllLines(filePath));
    }

    // Save products to file
    static void SaveProducts(List<string> products)
    {
        File.WriteAllLines(filePath, products);
    }

    // Add a product to the list
    static void AddProduct(List<string> products)
    {
        Console.Write("Enter the product name: ");
        string productName = Console.ReadLine();
        if (!string.IsNullOrEmpty(productName))
        {
            products.Add(productName);
            Console.WriteLine("Product added successfully.");
        }
        else
        {
            Console.WriteLine("Product name cannot be empty.");
        }
    }

    // Edit a product from the list
    static void EditProduct(List<string> products)
    {
        ShowProducts(products);

        if (products.Count > 0)
        {
            Console.Write("Enter the product number to edit: ");
            if (int.TryParse(Console.ReadLine(), out int productIndex) && productIndex > 0 && productIndex <= products.Count)
            {
                Console.Write("Enter the new product name: ");
                string newProductName = Console.ReadLine();
                if (!string.IsNullOrEmpty(newProductName))
                {
                    products[productIndex - 1] = newProductName;
                    Console.WriteLine("Product updated successfully.");
                }
                else
                {
                    Console.WriteLine("Product name cannot be empty.");
                }
            }
            else
            {
                Console.WriteLine("Invalid product number.");
            }
        }
    }

    // Show all products with a counter
    static void ShowProducts(List<string> products)
    {
        Console.WriteLine("\nProduct List:");
        if (products.Count == 0)
        {
            Console.WriteLine("No products available.");
        }
        else
        {
            for (int i = 0; i < products.Count; i++)
            {
                Console.WriteLine($"{i + 1}. {products[i]}");
            }
        }
    }
}
