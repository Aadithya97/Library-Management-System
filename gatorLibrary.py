# File: final.py
# Author: Aadithya Kandeth
# Email: aadithya.kandeth@ufl.edu
# UFID: 6980-2791

'''
COP5536 - Advanced Data Structures
Programming Project
GatorLibrary Management System
GatorLibrary is a fictional library that needs a software system to efficiently manage its books, patrons,
and borrowing operations.
The system should utilize a Red-Black tree data structure to ensure efficient management of the books.
Implement a priority-queue mechanism using Binary Min-heaps as a data structure for managing book
reservations in case a book is not currently available to be borrowed. Each book will have its own
min-heap to keep track of book reservations made by the patrons
'''

# Import necessary modules
import sys
import time
from os.path import splitext

# Class representing a node in the book tree
class BookNode:
    def __init__(self, bookId, bookName, authorName, isAvailable):
        # Initialize book node attributes
        self.bookId = bookId
        self.bookName = bookName
        self.authorName = authorName
        self.isAvailable = isAvailable
        self.borrowing_patron = None
        # Initializing reservations as a binary min heap
        self.reservations = BinaryMinHeap()

    # Method to get all reservations
    def get_reservations(self):
        reservations = []
        while True:
            minNode = self.reservations.remove_min()
            if minNode is not None:
                patronId = minNode[1]
                reservations.append(patronId)
            else:
                break
        return reservations # return reservations
    
    # Method to add a reservation to the book node for each book
    def add_reservation(self, patronId, priorityNumber):
        timestamp = time.time()
        # Create a reservation tuple
        reservation = (priorityNumber, patronId, timestamp)
         # Insert reservation into the binary min heap
        self.reservations.insert(reservation)

        # Limiting the number of reservations
        if len(self.reservations.heap) > 20:
            # Return message if the reservation limit is reached
            return "Waitlist full"
    
    # Method to remove the reservation with the highest priority
    def remove_reservation(self):
        return self.reservations.remove_min() if self.reservations.heap else None
    
    
    

# Class definition for a node in the Red-Black Tree
class RedBlackNode:
    #Constructor for RedBlackTree Node
    def __init__(self, val: BookNode):
        self.val = val
        # Initialize the node as black
        self.red = False
        self.parent = None
        self.left = None
        self.right = None

class RedBlackTree:
    #Constructor for RedBlackTree
    def __init__(self):
        # First Empty node for the tree
        self.nil = RedBlackNode(BookNode(0,None,None,None))
        self.nil.red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil
        self.color_flip_count = 0  # Initializing the flipCounter for color flips to 0

    # Method to insert a value into the Red-Black Tree
    def insert(self, val):
        #Binary Search Insertion
        new_node = RedBlackNode(val)
        # new node must be red
        new_node.red = True  
        new_node.parent = None
        new_node.left = self.nil
        new_node.right = self.nil

        parent = None
        current = self.root
        while current != self.nil:
            parent = current
             # Determine whether to move left or right based on the bookId of the new node
            if new_node.val.bookId < current.val.bookId:
                current = current.left
            elif new_node.val.bookId > current.val.bookId:
                current = current.right
            else:
                return

        # Set the parent and insert the new node
        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.val.bookId < parent.val.bookId:
            parent.left = new_node
        else:
            parent.right = new_node

        # Fix the tree
        self.post_insert_rotations(new_node)

    #Handle each rotation type if required after the insert is complete
    def post_insert_rotations(self, new_node):
        while new_node != self.root and new_node.parent.red:
            if new_node.parent == new_node.parent.parent.right:
                uncle = new_node.parent.parent.left  # uncle node
                if uncle.red:
                    uncle.red = False 
                    new_node.parent.red = False 
                    new_node.parent.parent.red = True 
                    if uncle == self.root or new_node.parent == self.root or new_node.parent.parent == self.root:
                        self.color_flip_count += 2 # Increment count of color flip
                    else:
                        self.color_flip_count += 3  # Increment count of color flip
                    new_node = new_node.parent.parent
                   
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotateRight(new_node)
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    if new_node.parent == self.root or new_node.parent.parent == self.root:
                        if self.root.red == True:
                            self.color_flip_count += 2
                        else:
                            self.color_flip_count += 1 # Increment count of color flip
                    else:
                        self.color_flip_count += 2 # Increment count of color flip
                    self.rotateLeft(new_node.parent.parent)
            else:
                uncle = new_node.parent.parent.right  # uncle
                if uncle.red:
                    uncle.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    if uncle == self.root or new_node.parent == self.root or new_node.parent.parent == self.root:
                        self.color_flip_count += 2 # Increment count of color flip
                    else:
                        self.color_flip_count += 3  # Increment count of color flip
                    new_node = new_node.parent.parent
                    
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotateLeft(new_node)
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    if new_node.parent == self.root or new_node.parent.parent == self.root:
                        if self.root.red == True:
                            self.color_flip_count += 2
                        else:
                            self.color_flip_count += 1 # Increment count of color flip
                    else:
                        self.color_flip_count += 2 # Increment count of color flip
                    self.rotateRight(new_node.parent.parent)
        self.root.red = False #reset root to black 

    #Method to delete a node from the red black tree
    def delete(self, val):
        # Dict_start holds all values of the node colors before the deletion
        dict_start = {}
        valList = []
        node = self.root
        valList.append(node)
        while valList:
            currNode = valList.pop(0)
            dict_start[currNode.val.bookId] = 1 if currNode.red else 0 # Add value as 1 for red and 0 for black
            if currNode.left:
                valList.append(currNode.left)
            if currNode.right:
                valList.append(currNode.right)
        z = self.find(val)
        if z is None:
            return

        # Deletion logic
        y = z
        y_original_color = y.red
        if z.left == self.nil:
            x = z.right
            self.node_transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.node_transplant(z, z.left)
        else:
            #(print("Here1 - delete"))
            y = self.minimum(z.right)
            y_original_color = y.red
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                #print("Here2 - delete")
                self.node_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.node_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.red = z.red

        if y_original_color == False:
            self.post_delete_rotations(x,dict_start)
        else:
            #Dict_end holds all values of the node colors after the deletion
            dict_end = {}
            valList = []
            node = self.root
            valList.append(node)
            while valList:
                currNode = valList.pop(0)
                dict_end[currNode.val.bookId] = 1 if currNode.red else 0
                if currNode.left:
                    valList.append(currNode.left)
                if currNode.right:
                    valList.append(currNode.right)
            #Calculate the number of nodes that have different values between dict_start and dict_end to get color flips. 
            colorDiff = {x : dict_start[x] == dict_end[x] for x in dict_start if x in dict_end }
            flipCounter = 0
            for diff in colorDiff.values():
                if diff == False:
                    flipCounter +=1
            self.color_flip_count += flipCounter

    #Method that handles rotations in the RBT post deletion
    def post_delete_rotations(self, x, dict_start):
        while x != self.root and x.red == False:
            if x == x.parent.left:
                w = x.parent.right
                if w.red:
                    w.red = False
                    x.parent.red = True
                    self.rotateLeft(x.parent)
                    w = x.parent.right

                if w.left.red == False and w.right.red == False:
                    w.red = True
                    x = x.parent
                else:
                    if w.right.red == False:
                        w.left.red = False
                        w.red = True
                        self.rotateRight(w)
                        w = x.parent.right

                    w.red = x.parent.red
                    x.parent.red = False
                    w.right.red = False
                    self.rotateLeft(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.red:
                    w.red = False
                    x.parent.red = True
                    self.rotateRight(x.parent)
                    w = x.parent.left

                if w.right.red == False and w.left.red == False:
                    w.red = True
                    x = x.parent
                else:
                    if w.left.red == False:
                        w.right.red = False
                        w.red = True
                        self.rotateLeft(w)
                        w = x.parent.left
                    
                    w.red = x.parent.red

                    x.parent.red = False
                    w.left.red = False
                    self.rotateRight(x.parent)
                    x = self.root
        x.red = False #reset node to black

        #Dict_end holds all values of the node colors after the deletion
        dict_end = {}
        valList = []
        node = self.root
        valList.append(node)
        while valList:
            currNode = valList.pop(0)
            dict_end[currNode.val.bookId] = 1 if currNode.red else 0
            if currNode.left:
                valList.append(currNode.left)
            if currNode.right:
                valList.append(currNode.right)

        #Calculate the number of nodes that have different values between dict_start and dict_end to get color flips. 
        colorDiff = {x : dict_start[x] == dict_end[x] for x in dict_start if x in dict_end }
        flipCounter = 0
        for diff in colorDiff.values():
            if diff == False:
                flipCounter +=1
        self.color_flip_count += flipCounter
        #The number of color flipped nodes is stored

    #Method that finds a node in the RedBlackTree and checks if it exists
    def find(self, val):
        val = int(val)
        currNode = self.root
        while currNode != self.nil and val != currNode.val.bookId: #iterating through each node
            if val < currNode.val.bookId:
                currNode = currNode.left
            elif val:
                currNode = currNode.right
        if currNode == self.nil:
            return None  # Does not exist
        else:
            return currNode # Return the found node
        
    # rotate right at a given node x
    def rotateRight(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # rotate left at a given node x
    def rotateLeft(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
 
    # Helper Method for facilitating swapping of two subtrees rooted at x and y
    def node_transplant(self, x, y):
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.parent = x.parent
    #Helper method for finding the min value node in the tree
    def minimum(self, x):
        while x.left != self.nil:
            x = x.left #min value is always to the left subtree
        return x



class ReservationNode:
    # Constructor to initialize a reservation node 
    def __init__(self, patronId, priorityNumber, reservationTime):
        self.patronId = patronId
        self.priority = priorityNumber
        self.reservationTime = reservationTime # Timestamp when reservation was made 

# Class that implements the Binary Min Heap
class BinaryMinHeap:
    #Constructor
    def __init__(self):
        self.heap = []

    def __iter__(self):
        return iter(self.heap)
    
    #Insert an element into the element
    def insert(self, element):
        self.heap.append(element)
        self.heapify_up(len(self.heap) - 1)

    #Remove top element from the heap
    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        top = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down()
        return top
    
    #Remove minimum element from the heap
    def remove_min(self):
        if not self.heap:
            return None
        min_element = self.heap[0]
        last_element = self.heap.pop()
        if self.heap:
            self.heap[0] = last_element
            self.heapify_down()
        return min_element
    
    #Get all elements in the heap
    def get_elements(self):
        return self.heap

    # Heapify up to maintain heap property
    def heapify_up(self, curr_idx):
        while curr_idx > 0:
            parent_idx = (curr_idx - 1) // 2
            if self.heap[parent_idx][0]> self.heap[curr_idx][0] or (
                    self.heap[parent_idx][0] == self.heap[curr_idx][0] and
                    self.heap[parent_idx][2] > self.heap[curr_idx][2]):
                self.swap(parent_idx, curr_idx)
                curr_idx = parent_idx
            else:
                break

    # Heapify down to maintain heap property
    def heapify_down(self):
        curr_idx = 0
        while True:
            lchild_idx = 2 * curr_idx + 1
            rchild_idx = 2 * curr_idx + 2
            smallestVal = curr_idx

            if lchild_idx < len(self.heap) and (
                    self.heap[lchild_idx][0] < self.heap[smallestVal][0] or (
                    self.heap[lchild_idx][0] == self.heap[smallestVal][0] and
                    self.heap[lchild_idx][2] < self.heap[smallestVal][2])):
                smallestVal = lchild_idx

            if rchild_idx < len(self.heap) and (
                    self.heap[rchild_idx][0] < self.heap[smallestVal][0] or (
                    self.heap[rchild_idx][0] == self.heap[smallestVal][0] and
                    self.heap[rchild_idx][2] < self.heap[smallestVal][2])):
                smallestVal = rchild_idx

            if smallestVal != curr_idx:
                self.swap(curr_idx, smallestVal)
                curr_idx = smallestVal
            else:
                break
    
    # Swap elements 
    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]


# Class for the library management system
class LibraryManagementSystem:
    def __init__(self):
        self.bookTree = RedBlackTree() # Red black tree to store books
        self.patrons = {} # Dictionary to store patrons 

    # Exit the program
    def quit(self):
        exit()

    # Add a new book
    def add_book(self, bookId, bookName, authorName, isAvailable):
        newBook = BookNode(bookId, bookName, authorName, isAvailable)
        self.bookTree.insert(newBook) # Insert book node into tree

    # Print details of a book
    def print_book(self, bookId):
        node = self.bookTree.find(bookId)
        if node is not None:
            patron_ids = [patronId[1] for patronId in node.val.reservations.heap]
            details = (
                f"BookID = {node.val.bookId}\n"
                f"Title = {node.val.bookName}\n"
                f"Author = {node.val.authorName}\n"
                f"Availability = {node.val.isAvailable}\n"
                f"BorrowedBy = {node.val.borrowing_patron}\n"
                f"Reservations = {patron_ids}"
            )
            return details
        else:
            return (f"Book {bookId} not found.")

    # Print details of all books in the range id1 to id2
    def print_books(self, node, book_id1, book_id2):
        books_details = []  # List to store details of books
        def process_book(book_node):
            patron_ids = [patronId[1] for patronId in book_node.val.reservations.heap]
            details = (
                f"BookID = {book_node.val.bookId}\n"
                f"Title = {book_node.val.bookName}\n"
                f"Author = {book_node.val.authorName}\n"
                f"Availability = {book_node.val.isAvailable}\n"
                f"BorrowedBy = {book_node.val.borrowing_patron}\n"
                f"Reservations = {patron_ids}"
            )
            books_details.append(details)
        def inorder_traversal(node):
            nonlocal books_details
            if node is not None:
                inorder_traversal(node.left)
                if isinstance(node.val, BookNode) and book_id1 <= node.val.bookId <= book_id2:
                    process_book(node)
                inorder_traversal(node.right)
        inorder_traversal(node)
        return books_details

    # Insert a new book
    def insert_book(self, bookId, bookName, authorName, isAvailable, borrowing_patron=None,
                    reservation_heap=None):
        newBook = BookNode(bookId, bookName, authorName, isAvailable)
        newBook.isAvailable = isAvailable
        newBook.borrowing_patron = borrowing_patron
        if reservation_heap:
            newBook.reservations.heap = reservation_heap
        self.bookTree.insert(newBook) # Insert into tree

    # Handle book borrowing
    def borrow_book(self, patronId, bookId, patron_priority):
        node = self.bookTree.find(bookId)

        if node is not None:
            if node.val.isAvailable == '"Yes"':
                # If available, lend book
                node.val.isAvailable = '"No"'
                node.val.borrowing_patron = patronId
                self.patrons
                return f"Book {bookId} Borrowed by Patron {patronId}"

            else:
                # If not available, add a reservation for that patron
                reservation_added = node.val.add_reservation(patronId, patron_priority)
                if reservation_added == "Waitlist full":
                    return f"Waitlist for Book {bookId} is full. Cannot add reservation for Patron {patronId}"
                else:
                    return f"Book {bookId} Reserved by Patron {patronId}"

        else:
            return f"Book {bookId} is not available for borrowing."

    # Handle book return
    def return_book(self, patronId, bookId):
        node = self.bookTree.find(bookId)
        opLine = ''
        if node is not None and node.val.isAvailable == '"No"' and node.val.borrowing_patron == patronId:
            if len(node.val.reservations.heap) > 0: #If valid heap, handle reservations if any
                reserved_patron_id = node.val.reservations.heap.pop(0)
                node.val.borrowing_patron = reserved_patron_id[1]
                opLine = f"Book {bookId} Returned by Patron {patronId}\n\n\n" \
                f"Book {bookId} Allotted to Patron {node.val.borrowing_patron}"
            else:
                node.val.isAvailable = '"Yes"'
                node.val.borrowing_patron = None
                opLine = f"Book {bookId} Returned by Patron {patronId}"

        else:
            opLine = f"Book {bookId} cannot be returned by Patron {patronId}."
        return opLine

    # Delete a book
    def delete_book(self, bookId):
        node = self.bookTree.find(bookId)
        if node is not None:
            if node.val.reservations.heap:
                reservations = node.val.get_reservations()
                self.cancel_reservations(bookId, reservations)
                opLine = f"Book {bookId} is no longer available. Reservations made by Patrons {', '.join(str(reservation) for reservation in reservations)} have been cancelled!"
            else:
                opLine = f"Book {bookId} is no longer available."
            self.bookTree.delete(bookId)
        else:
            opLine = f"Book {bookId} not found."
        return opLine

    # Search for a book
    def search_book(self, node, bookId):
        while node != None and bookId != node.bookId: #use binary search to find the book
            if bookId < node.bookId:
                node = node.left
            else:
                node = node.right
        return node
    
    #Find the closest two books to a target book. 
    def find_closest_book(self, node, target):
        lowerBook, higherBook = self.findClosestBookHelper(node, target) # Find closest two books
        books_details = []

        if lowerBook is not None and higherBook is not None:
            distance_lower = abs(target - lowerBook.val.bookId)
            distance_higher = abs(target - higherBook.val.bookId)
            if distance_lower < distance_higher:
                details = self.get_book_details(lowerBook)
                books_details.append(details)
            elif distance_higher < distance_lower:
                details = self.get_book_details(higherBook)
                books_details.append(details)
            else:
                # Equal distances, return both closest books
                if lowerBook.val.bookId == higherBook.val.bookId:
                    details = self.get_book_details(lowerBook)
                    books_details.append(details)
                else :
                    details1 = self.get_book_details(lowerBook)
                    details2 = self.get_book_details(higherBook)
                    books_details.append(details1)
                    books_details.append(details2)

        elif lowerBook is not None:
            details = self.get_book_details(lowerBook)
            books_details.append(details)
        elif higherBook is not None:
            details = self.get_book_details(higherBook)
            books_details.append(details)

        return books_details
    
    #Helper function for finding closest two books
    def findClosestBookHelper(self, node, target, lowerBook=None, higherBook=None):
        while node.val.bookId != 0:
            if node.val.bookId == target:
                return node, node   # if the node val equals the target, return the node itself as closest.
            elif node.val.bookId < target:
                lowerBook = node
                node = node.right
            else:
                higherBook = node
                node = node.left
        return lowerBook, higherBook  #return closest lower and higher nodes

    # Get book details 
    def get_book_details(self, node):
        patron_ids = [patronId[1] for patronId in node.val.reservations.heap]
        return (
            f"BookID = {node.val.bookId}\n"
            f"Title = {node.val.bookName}\n"
            f"Author = {node.val.authorName}\n"
            f"Availability = {node.val.isAvailable}\n"
            f"BorrowedBy = {node.val.borrowing_patron}\n"
            f"Reservations = {patron_ids}"
        )
    
    # Cancel reservations
    def cancel_reservations(self, bookId, patrons):
        for patronId in patrons: # Cancel reservations of given patrons
            patron = self.patrons.get(patronId, None)
            if patron is not None:
                patron.cancel_reservation(bookId)

    # Return the color flip count that is calculated during program execution
    def color_flip_count(self):
        return self.bookTree.color_flip_count


def main(input_file_name):
    #Create a LibraryManagementSstem object
    library = LibraryManagementSystem()
    # Read input from the passed file (input.txt)
    with open(input_file_name, "r") as file:
        lines = file.readlines()
        output_lines = []

        # Parse Command String
        def parseCommand(command_string):
            parts = command_string.split('(')
            comm = parts[0].strip()
            if len(parts) > 1:
                inputArgs = parts[1].rstrip(')').split(',')
                inputArgs = [arg.strip() for arg in inputArgs]
                return comm, inputArgs #Return command along with the argument list
            else:
                return comm, []

        
        for l in lines:
            l = l.strip() #Removing whitespace
            output_line = None

            if l == "Quit()": #check for quit and handle 
                output_line = f"Program Terminated!!"
                output_lines.append(output_line)
                break

            else: #parse the command string
                comm, *args = parseCommand(l)
                print(comm)
                args = args[0]
                #Handle each case of command as specified in the description. Call the respective method
                if comm == "InsertBook":
                    bookId, title, author, isAvailable = args[0],args[1],args[2],args[3]
                    library.insert_book(int(bookId), title, author, isAvailable, None, None)
                elif comm == "PrintBook":
                    bookId = args[0]
                    output_line = library.print_book(bookId)
                elif comm == "PrintBooks":
                    book_id1, book_id2 = args[0], args[1]
                    books = library.print_books(library.bookTree.root, int(book_id1), int(book_id2))
                    all_books = [
                        f"{book}\n" for book in books]
                    # Join lines and print 
                    output_line = '\n'.join(all_books)
                elif comm == "FindClosestBook":
                    target = args[0]
                    closest_books = library.find_closest_book(library.bookTree.root, int(target))
                    all_closest_books = [
                        f"{book}\n" for book in closest_books]
                    # Join lines and print 
                    output_line = '\n'.join(all_closest_books)
                elif comm == "BorrowBook":
                    patronId, bookId, priority = args[0], args[1], args[2]
                    output_line = library.borrow_book(int(patronId), int(bookId), int(priority))
                elif comm == "ReturnBook":
                    patronId, bookId = args
                    output_line = library.return_book(int(patronId), int(bookId))
                elif comm == "DeleteBook":
                    bookId = args[0]
                    output_line = library.delete_book(int(bookId))
                elif comm == "ColorFlipCount":
                    output_line = f"Colour Flip Count: {library.bookTree.color_flip_count}"

            if output_line is not None:
                #Append to output file
                output_lines.append(output_line)
                output_lines.append("\n")

    # Write output to a text file
    try:
        # Create output file based on the input filename
        output_filename = splitext(input_file_name)[0] + "_output_file.txt"

        # Write the output content to the output file
        with open(output_filename, 'w') as output_file:
            for l in output_lines:
                output_file.write(str(l) + '\n')
    #Exception handling
    except Exception as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use Syntax: python3 gator.py input_file_name")
        sys.exit(1)
    input_file_name = sys.argv[1]
    main(input_file_name)
