    main_menu_button.draw(screen)

    if main_menu_button.submenu_open:
        pygame.draw.rect(screen, (200, 200, 200), (0, 45, 400, 70))  
        submenu_options = [lamp_option, battery_option, key_option]
        for option in submenu_options:
            option.draw(screen)