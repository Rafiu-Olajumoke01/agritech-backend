import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import User from '../models/userModel.js'; 

// ✅ Register User
export const registerUser = async (req, res) => {
  try {
    const { fullName, email, phone, location, password, role } = req.body;

    // Check if user already exists in MongoDB
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ message: 'Email already in use' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create new user in MongoDB
    const user = await User.create({
      fullName,
      email,
      phone,
      location,
      password: hashedPassword,
      role,
    });

    res.status(201).json({
      message: 'User registered successfully',
      user,
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

// ✅ Login User
export const loginUser = async (req, res) => {
  try {
    const { email, password } = req.body;

    // Find user in MongoDB
    const user = await User.findOne({ email });
    if (!user)
      return res.status(400).json({ message: 'Invalid email or password' });

    // Compare passwords
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch)
      return res.status(400).json({ message: 'Invalid email or password' });

    // Generate JWT token
    const token = jwt.sign(
      { id: user._id, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: '1d' }
    );

    res.status(200).json({
      message: 'Login successful',
      token,
      user,
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

// ✅ Get All Users
export const getAllUsers = async (req, res) => {
  try {
    const users = await User.find().select('-password'); 
    res.status(200).json({
      message: 'All users fetched successfully',
      users,
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};
