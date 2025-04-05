/*
    Write a function isPalindrome(str) that checks if a given string is a palindrome (reads the same backward as forward).
*/

const args = process.argv.slice(2);  // Slice starts from 2 to exclude the first two elements (node and script name)
let reversed = '';  // Initialize reversed as an empty string

for (let i = 0; i < args[0].length; i++) {
    reversed = args[0][i] + reversed;
}

console.log("Input string: " + args[0]);        // Print the original string
console.log("Reversed string: " + reversed);    // Print the reversed string
if(args[0]===reversed)
    console.log("The string is a palindrome");
else
    console.log("The string is NOT a palindrome");
