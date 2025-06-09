// import React from "react";
import {
    Box,
    Container,
    Typography,
    Button,
    // Stack,
    // AppBar,
    // Toolbar,
    // Link
} from "@mui/material";

function Dashboard() {
    return (
        <Box
            sx={{
                backgroundImage: 'url("https://image.tmdb.org/t/p/original/8Y43POKjjKDGI9MH89NW0NAzzp8.jpg")',
                backgroundSize: "cover",
                backgroundPosition: "center",
                color: "white",
                py: 10,
                px: 2,
                textAlign: "center",
            }}
        >
            <Container maxWidth="md">
                <Typography variant="h2" fontWeight="bold" gutterBottom>
                    Welcome to Flixbook
                </Typography>
                <Typography variant="h5" mb={4}>
                    Your personal movie tracker
                </Typography>
                <Button variant="contained" color="primary" size="large" href="/movies">
                    Browse Movies
                </Button>
            </Container>
        </Box>
    );
}

export default Dashboard;