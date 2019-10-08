import numpy as np
import trajectory_planning_helpers.path_matching_local
import trajectory_planning_helpers.get_rel_path_part
import typing


def path_matching_global(path_cl: np.ndarray,
                         ego_position: np.ndarray,
                         s_expected: typing.Union[float, None] = None,
                         s_range: float = 20.0) -> tuple:
    """
    Created by:
    Alexander Heilmeier

    Documentation:
    Get the corresponding s coordinate and the displacement of the own vehicle in relation to the global path.

    Inputs:
    path_cl:        Closed path used to match ego position ([s, x, y]).
    ego_position:   Ego position of the vehicle ([x, y]).
    s_expected:     Expected s position of the vehicle in m.
    s_range:        Range around expected s position of the vehicle to search for the match in m.

    Outputs:
    s_interp:       Interpolated s position of the vehicle in m. The following holds: s_interp in range [0.0,s_tot[.
    d_displ:        Estimated displacement from the trajectory in m.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # GET RELEVANT PART OF PATH FOR EXPECTED S -------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # get s_tot into a variable
    s_tot = path_cl[-1, 0]

    if s_expected is not None:
        path_rel = trajectory_planning_helpers.get_rel_path_part.get_rel_path_part(path_cl=path_cl,
                                                                                   s_pos=s_expected,
                                                                                   s_dist_back=s_range,
                                                                                   s_dist_forw=s_range)

        # path must not be considered closed specifically as it is continuous and unclosed by construction
        consider_as_closed = False

    else:
        path_rel = path_cl[:-1]

        # path is unclosed to keep every point unique but must be considered closed to get proper matching between
        # last and first point
        consider_as_closed = True

    # ------------------------------------------------------------------------------------------------------------------
    # USE PATH MATCHING FUNCTION ON RELEVANT PART ----------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # get s_interp and d_displ
    s_interp, d_displ = trajectory_planning_helpers.path_matching_local.\
        path_matching_local(path=path_rel,
                            ego_position=ego_position,
                            consider_as_closed=consider_as_closed,
                            s_tot=s_tot)

    # cut length if bigger than s_tot
    if s_interp >= s_tot:
        s_interp -= s_tot

    # now the following holds: s_interp -> [0.0; s_tot[

    return s_interp, d_displ


# testing --------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass