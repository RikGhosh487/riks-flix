import axios, { type AxiosResponse } from 'axios';
import { API_BASE_URL } from './config';

export interface MovieGridData {
    id: number;
    title: string;
    releaseYear: number;
    duration: number;
    rating: number;
    mpaaRating: string;
    posterUrl: string;
    slug: string;
}

// Get all the movies
export const getMovies = async () : Promise<MovieGridData[]> => {
    const response: AxiosResponse<MovieGridData[]> = await axios.get(`${API_BASE_URL}/movies`, {
    });

    console.log("Movies fetched:", response.data);

    return response.data;
}