### README for Hello Home Web Application

---

#### **Project Name**  
Hello Home Web Application  

#### **Purpose**  
Hello Home is a real estate web platform designed to connect users and agents for efficient property transactions. Users can list, edit, and manage real estate properties for sale or rent, while agents handle larger-scale deals and property management.  

---

### **Features**
1. **User Registration and Login**  
   - Register as a user or agent with personal details.  
   - Secure login for accessing personalized features.

2. **Property Management**  
   - Add, update, and delete property listings with images.  
   - Manage property availability (rented, sold, or available).  

3. **Property Browsing and Details**  
   - View properties for rent or sale.  
   - Access detailed information about properties, including price, area, amenities, and images.  

4. **User Reviews**  
   - Submit reviews and ratings for listed properties.  
   - View reviews by other users to make informed decisions.  

5. **Profile Management**  
   - View and edit personal profile details, including profile picture and contact information.

6. **Session Management**  
   - Secure session handling with login, logout, and automatic session expiration.  

---

### **Target Audience**
- **Home Buyers**: Browse property listings and contact agents.  
- **Sellers**: Manage and list real estate properties.  
- **Real Estate Agents**: Oversee listings, manage client relations, and handle property transactions.

---

### **Technical Stack**

#### **Backend**  
- Python (Flask Framework)  
- SQLite Database  

#### **Frontend**  
- HTML, CSS, Bootstrap  

#### **Server and Hosting**  
- Application Server: Gunicorn  
- Web Server: Nginx  
- Hosting: AWS EC2  

---

### **Database Design**

#### Core Tables:  
1. **Accounts Table**  
   - Stores user/agent details such as name, email, phone, username, password, and role.

2. **Properties Table**  
   - Tracks property details like price, area, images, and availability.

3. **Reviews Table**  
   - Captures user reviews and ratings for properties.

---

### **Setup Instructions**

#### **Development Environment**
1. Install Python 3.x.  
2. Install required libraries: `sudo apt install nginx`.
3. Install Gunicorn: `sudo apt install gunicorn`.
4. Install Flask Framework: `pip install flask`. 
5. Run the development server: `python app.py`.

#### **Deployment**
1. Use AWS EC2 with Ubuntu OS.  
2. Install and configure Flask, Gunicorn, and Nginx.  
3. Upload project files to the server.  
4. Configure the web server for deployment.  

For detailed deployment instructions, refer to the *Deployment Process* section in the project documentation.

---

### **Key Functionalities**

1. **Add Property**  
   - Submit property details with support for multiple images.  

2. **Update Property**  
   - Edit property details and add new images.

3. **Delete Property**  
   - Remove property listings upon sale or unavailability.

4. **Property Listings**  
   - Browse all available properties with filtering options.

5. **View Details**  
   - See detailed property information with image carousels.

6. **Reviews**  
   - Add and read reviews for listed properties.  

---

### **System Design**

1. **Authentication and Authorization**  
   - Role-based access for users and agents.  
   - Secure sessions to protect sensitive actions.

2. **File Handling**  
   - Image uploads for property listings.  
   - Storage in the server directory.  

3. **Session Management**  
   - Automatic session timeout for inactive users.


---

### **Contributing**
1. Fork the repository.  
2. Create a feature branch.  
3. Commit changes and submit a pull request.  

--- 

