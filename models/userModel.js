import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
    fullName: {
        type: String,
        required: [true, 'Fullname is required'],
        trim: true
    },

    email: {
        type: String,
        required: [true, 'Email is required'],
        unique: true,
        lowercase: true
    },

    phone: {
        type: String,
        required: [true, 'Phone number is required']
    },
    location: {
        type: String,
        required: [true, 'Location is required']
    },
    password: {
        type: String,
        required: [true, 'Password is required'],
        minlength: [6, 'Password must be at least 6 characters']
    },
    role: {
        type: String,
        enum: ['farmer', 'buyer'],
        required: true
    },
},
    { timestamps: true }
)

const User = mongoose.model('User', userSchema)
export default User;