#include "pch.h"
#include <iostream>
#include <Windows.h>

#define ISRAEL 117
/*
	Figures the current configured home location of current running user.
	Returns 1 if Israel is configured as Home location for current user, else returns 0;
*/
int main()
{
	GEOCLASS ret = GetUserGeoID(GEOCLASS_NATION);
	return ret == ISRAEL;
}
