// imports for the component
import { AppBar, Toolbar, Button, Tooltip, Switch } from "@mui/material";
import NightlightIcon from "@mui/icons-material/Nightlight";

export interface NavBarProps {
    /** The navigational endpoints */
    navItems: string[];

    /** Optional: Dark mode toggle */
    darkMode?: boolean;
}

export const NavBar = ({ navItems, darkMode } : NavBarProps) => {
    return (
        <AppBar position="sticky">
            <Toolbar sx={{ display: "flex", flexDirection: "row-reverse" }}>
                <Tooltip title="Toggle Dark Mode" arrow>
                    <span style={{ display: "flex", alignItems: "center" }}>
                        <Switch checked={darkMode} color="default" />
                        <NightlightIcon />
                    </span>
                </Tooltip>
                {navItems.reverse().map((item, idx) => (
                    <Button key={idx} color="inherit">
                        {item}
                    </Button>
                ))}
            </Toolbar>
        </AppBar>
    );
};
