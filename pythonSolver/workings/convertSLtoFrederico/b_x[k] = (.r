b_x[k] =   ( 
                ((Lambda/(3*dy))+(mu/(3*dx)))*(u_previous[k+nx+1,1] - v_left) - ((mu + Lambda)/dy)*(u_previous[k+nx,0] - 3*u_previous[k,0] + 2*u_bottom ) )*Sfx - (rho/(dt**2))*(u_old_old[k,0] - 2*u_old[k,0])*dx*dy
                 + 2*u_left*a_W + 2*u_bottom*a_S

b_x[k] =(
            (rho/(dt**2))*( 2*(u_old[k,0])*dx*dy - u_old_old[k,0]*dx*dy) 
            + (Sfy/dy)*(2*mu)*u_bottom       # should this be lambda?
            + (Sfx/dx)*(4*mu +2*Lambda)*u_left
            + (Sfy/(3*dx))*mu*( 
                                + u_previous[k+1,1] 
                                +  u_previous[k+1+nx, 1]
                                - 2*v_left
                                )
            + (Sfx/(3*dy))*Lambda*( 
                                    + u_previous[k+nx , 1]
                                    + u_previous[k+1+nx , 1]
                                    - 2*v_bottom
                                    )
        ) + (
            (Sfy/dy)*(3*mu + 3*Lambda)*u_previous[k, 0]    # from ap frederico
            -(Sfy/dy)*(mu + Lambda)*u_previous[k+nx, 0]    # an frederico
            ) # an frederico





            -2*mu -2*lambda + 2((2*mu + Lambda))

            