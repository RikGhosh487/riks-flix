import type { Meta, StoryObj } from "@storybook/react-vite";

import { NavBar } from "../NavBar";

const meta = {
    title: "Components/NavBar",
    component: NavBar,
    tags: ["autodocs"],
} satisfies Meta<typeof NavBar>;

export default meta;
type Story = StoryObj<typeof NavBar>;

export const Default: Story = {
    args: {
        navItems: ["Home", "Movies", "About"],
        darkMode: false,
    },
};